import os
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings #langchain==0.0.332 is needed for this to work properly
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

from operator import itemgetter

openai_api_key = os.environ["OPENAI_API_KEY"]

temperature = 0.0 
listing_example_llm = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key) 

# ---------- Define output data types within the Listings class and initialize a parser to capture the output ----------------- # 

class Listings(BaseModel):

    values: list = Field(description='real estate listing with Neighborhood, Price ($, without comma), Bedrooms (1-6), Bathrooms (1-6), House Size (sqft, without comma), Description, Neighborhood Description')

listings_parser = PydanticOutputParser(pydantic_object=Listings)

# ----------- Setup the request for llm call to generate real estate listings ---------------- #

human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
chat_prompt = ChatPromptTemplate.from_messages([human_prompt])

request = chat_prompt.format_prompt(
    request="Give me 4 imaginary and creative but realistic real estate listings with very long, descriptive, detailed Description and Neighborhood Description using the example:\n\n{input_example}",
    format_instructions=listings_parser.get_format_instructions()
).to_messages()

input_example = """
Neighborhood: Green Oaks
Price: $800,000
Bedrooms: 3
Bathrooms: 2
House Size: 2,000 sqft

Description: Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.

Neighborhood Description: Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze.
"""

# ----------- Make the llm call to create hypothetical listings and aggregate them and save the llm call results (hypothetical listings) in a csv file to avoid making multiple calls to the llm ---------------- #

# list_of_df_listings = []

# for _ in range(6):
#     results = listing_example_llm(request, temperature=0)
#     results_values = listings_parser.parse(results.content)

#     # print(results_values.values)
#     df_listings_t = pd.DataFrame(results_values.values)
#     list_of_df_listings.append(df_listings_t.copy())

# df_listings = pd.concat(list_of_df_listings, ignore_index=True, sort=False).drop_duplicates(subset=["Neighborhood"]).copy()

# df_listings.to_csv("./listings.csv", index=False)

# ----------- Load the listing examples from csv file -------------------#

loader = CSVLoader(file_path='./listings.csv')
docs = loader.load()

# -------------- Create and save the embeddings in a Chroma db -------------------#

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_docs = splitter.split_documents(docs)

db = Chroma.from_documents(split_docs, embeddings)

# ------------------ Capture user preference (in the form of a list of questions and answers) -------------- #
questions = [   
                "How big do you want your house to be?", 
                "What are 3 most important things for you in choosing this property?", 
                "Which amenities would you like?", 
                "Which transportation options are important to you?",
                "How urban do you want your neighborhood to be?",   
            ]
answers = [
    "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
    "A quiet neighborhood, good local schools, and convenient shopping options.",
    "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
    "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
    "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
            ]

# --------------- Summarize user preference ------------- #

user_preference_llm = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key) 

history = ChatMessageHistory()
history.add_user_message(f"""You are AI that will recommend user house listing based on their answers to preference questions. Ask user {len(questions)} questions""")
for i in range(len(questions)):
    history.add_ai_message(questions[i])
    history.add_user_message(answers[i])
    
conversation_with_summary = ConversationChain(
    llm=user_preference_llm,
    memory=ConversationSummaryMemory.from_messages(llm=user_preference_llm, chat_memory=history, return_messages=True),
    verbose=False
)
query = conversation_with_summary.predict(input="What is the user preference? Please highlight the most important things first")

# print(query)

# ---------------- Search vector database based on user preference ------------#

retrieved_listings = db.similarity_search(query, k=5) 

# print(retrieved_listings)

# ---------------- Create relevance score and filter out the listings with lower score ---------------- #

personalization_llm = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key) 

scoring_prompt = PromptTemplate(
        input_variables=["user_preference", "context"],
        template="""
        You are a helpful AI bot. Based on the {user_preference}, prioritizing the most important things, your goal is to provide a rating that is as close as possible to the score human would give to this {context}.
            Remember that human has very limited time and wants to see something they will like, so your score should be as accurate as possible.
            Score will range from 1 to 100, with 100 meaning human will love it, and 1 meaning human will hate it.
            YOUR OUTPUT SHOULD INCLUDE THE SCORE ONLY AND NOTHING ELSE.
            FOLLOW THE INSTRUCTIONS STRICTLY, OTHERWISE HUMAN WILL NOT BE ABLE TO UNDERSTAND.
        """

    )
scoring_chain = load_qa_chain(personalization_llm, prompt = scoring_prompt, chain_type="stuff")


list_of_relevant_listings = []

for listing in retrieved_listings:
    relevant_listing_dict = dict()
    score = scoring_chain.run(input_documents=[listing], user_preference = query)
    if int(score) >= 50: # Setting 50 as the threshold
        relevant_listing_dict["score"] = int(score)
        relevant_listing_dict["listing"] = listing

        list_of_relevant_listings.append(relevant_listing_dict.copy())

sorted_list_of_relevant_listings = sorted(list_of_relevant_listings, key=itemgetter('score'), reverse=True)

# ------- Present the personalized relevant listings to the user ----------------- #

personalization_prompt = PromptTemplate(
        input_variables=["user_preference", "context"],
        template="""
        You are a helpful AI bot. Based on the {user_preference}, prioritizing the most important things, your goal is to provide a personalizaed description of the {context}. Emphasize aspects of the context that align with what the user is looking for, tailoring it to resonate with the user’s specific preferences.
        Maintain Factual Integrity. Ensure that the personalization process enhances the appeal of the context without altering factual information. Stay within the facts mentioned in the context and avoid creating anything that does not exist in the context.
        Remember that user has very limited time and wants to see something they will like, so your personalized description should be as accurate as possible.
        YOUR OUTPUT SHOULD START WITH THE NEIGHBORHOOD NAME, FOLLOWED BY THE PERSONALIZED DESCRIPTION.
        FOLLOW THE INSTRUCTIONS STRICTLY, OTHERWISE USER WILL NOT BE ABLE TO UNDERSTAND.
        """

    )
personalization_chain = load_qa_chain(personalization_llm, prompt = personalization_prompt, chain_type="stuff")


print("Here are the suggested properties based on your preference:")

for relevant_listing in sorted_list_of_relevant_listings:

    print("Property highlights:")
    print(personalization_chain.run(input_documents=[relevant_listing["listing"]], user_preference = query))
    print("")
    print("Property details:")
    print(relevant_listing["listing"].page_content)
    print("======================================")
