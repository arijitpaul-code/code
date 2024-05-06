This gives an overview of the project submission. The entire project has been developed on VSCode on Ubuntu 24.04 and managed using Github (https://github.com/arijitpaul-code/code)

The Python code is in HomeMatch.py file
The hypothetical listings generated are in listings.csv file (the listings are generated using LLM, the code for which is in the HomeMatch.py)
The requirements.txt file is updated for the correct langchain==0.0.332 version to make this code work

The main code is as follows 

Defined doutput data types within the Listings class and initialize a pydantic parser to capture the output
Setup the request for llm call to generate real estate listings in batches of 4, otherwise listing descriptions were becoming short
Made the llm call to create hypothetical listings and aggregate them and save the llm call results (hypothetical listings) in a csv file to avoid making multiple calls to the llm
Loaded the listing examples from csv file
Created and saved the embeddings in a Chroma db
Captured user preference (in the form of a list of questions and answers)
Summarized user preference using LLM on the user preference Q&A
Searched vector database based on user preference summary
Created relevance score and filtered out the listings with lower score
Presented the personalized relevant listings to the user

Here is the output from one run:

Here are the suggested properties based on your preference:
Property highlights:
Sunset Ridge: Immerse yourself in the tranquil charm of Sunset Ridge, where suburban tranquility meets urban convenience. This cozy neighborhood boasts quiet streets perfect for peaceful living, while also offering easy access to a reliable bus line for stress-free commuting. The good local schools in the area provide excellent educational opportunities for families, and the proximity to convenient shopping options ensures that daily errands are a breeze. 

Sunset Ridge is a haven for outdoor enthusiasts, with bike-friendly roads that make it easy to explore the scenic surroundings. The neighborhood strikes a perfect balance between suburban serenity and access to urban amenities, with a variety of restaurants and theaters just a short drive away. 

In Sunset Ridge, you'll find the perfect blend of comfort and style in this modern ranch home. With a spacious kitchen ideal for culinary adventures, a cozy living room for relaxation, and a backyard oasis for gardening, this property truly embodies the user's preferences. The two-car garage provides ample storage space, while the modern, energy-efficient heating system ensures year-round comfort. Don't miss the opportunity to make Sunset Ridge your new home sweet home.

Property details:
Neighborhood: Sunset Ridge
Price: 600000
Bedrooms: 3
Bathrooms: 2
House Size: 2000
Description: Discover the perfect blend of comfort and style at this modern ranch home in Sunset Ridge. This 3 bedroom, 2 bathroom property features an open floor plan with high ceilings and hardwood floors throughout. The chef's kitchen is equipped with quartz countertops and a breakfast bar. The master suite offers a walk-in closet and a spa-like bathroom. The backyard oasis includes a covered patio and a fire pit, perfect for outdoor gatherings.
Neighborhood Description: Sunset Ridge is a sought-after neighborhood known for its friendly community and convenient location. Residents have access to parks, walking trails, and recreational facilities. The neighborhood is close to major highways, making it easy to commute to downtown and other parts of the city.
======================================
Property highlights:
Neighborhood: Enchanted Forest

Description: Welcome to the Enchanted Forest neighborhood, where you will find a charming cottage that meets all your preferences. This 4 bedroom, 3 bathroom home offers a cozy fireplace, hardwood floors, and a spacious backyard for gardening. The kitchen features granite countertops and stainless steel appliances, perfect for your culinary adventures. 

The Enchanted Forest neighborhood is a tranquil oasis with lush greenery and winding paths, providing a peaceful retreat from the hustle and bustle of the city. You'll have easy access to hiking trails, parks, and a strong sense of community. Local cafes and shops are just a short distance away, offering convenience without sacrificing the beauty of nature.

This neighborhood strikes the perfect balance between suburban tranquility and access to urban amenities, with restaurants and theaters within reach. With a focus on a quiet environment, good local schools, and convenient shopping options, the Enchanted Forest neighborhood is sure to meet all your needs.

Property details:
Neighborhood: Enchanted Forest
Price: 750000
Bedrooms: 4
Bathrooms: 3
House Size: 2800
Description: Welcome to this charming cottage nestled in the heart of the Enchanted Forest. This 4 bedroom, 3 bathroom home features a cozy fireplace, hardwood floors, and a spacious backyard perfect for entertaining. The kitchen boasts granite countertops and stainless steel appliances. Enjoy the tranquility of nature while being just a short drive away from the city.
Neighborhood Description: The Enchanted Forest neighborhood is known for its lush greenery, winding paths, and sense of magic. Residents enjoy access to hiking trails, parks, and a strong sense of community. Local cafes and shops are just a stone's throw away, making this neighborhood the perfect blend of nature and convenience.
======================================
Property highlights:
Neighborhood: Sunset Heights

Description: Welcome to Sunset Heights, where luxury meets tranquility. This prestigious neighborhood offers panoramic views of the city and mountains, perfect for those seeking a peaceful retreat. The community boasts top-rated schools, upscale dining options, and convenient shopping, catering to your desire for a quiet neighborhood with good local schools and convenient amenities. Sunset Heights is family-friendly, with parks, playgrounds, and walking trails for outdoor enjoyment. Experience the perfect balance of suburban tranquility and urban amenities in Sunset Heights.

Property details:
Neighborhood: Sunset Heights
Price: 950000
Bedrooms: 5
Bathrooms: 4
House Size: 3500
Description: Step into luxury in this stunning 5 bedroom, 4 bathroom home in Sunset Heights. The open concept floor plan is perfect for entertaining, with a gourmet kitchen, formal dining room, and a spacious living area. The master suite features a spa-like bathroom and a private balcony with breathtaking views. The backyard oasis includes a pool, hot tub, and outdoor kitchen.
Neighborhood Description: Sunset Heights is a prestigious neighborhood known for its panoramic views of the city and mountains. Residents enjoy easy access to top-rated schools, upscale dining, and shopping. The community is family-friendly with parks, playgrounds, and walking trails. Experience the best of luxury living in Sunset Heights.


