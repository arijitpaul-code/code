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
Sunset Ridge: Immerse yourself in the tranquil yet vibrant community of Sunset Ridge, where suburban charm meets urban convenience. This neighborhood offers a peaceful environment with easy access to parks, walking trails, and recreational facilities, perfect for those seeking a quiet and family-friendly atmosphere. Sunset Ridge is also strategically located near major highways, providing seamless commutes to downtown and beyond. Enjoy the best of both worlds with a friendly community and convenient amenities right at your doorstep.

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
Enchanted Forest Neighborhood:
Welcome to the Enchanted Forest neighborhood, where suburban tranquility meets urban convenience. This charming cottage offers 4 bedrooms, 3 bathrooms, and a cozy fireplace for those chilly evenings. Hardwood floors and a spacious backyard make this home perfect for entertaining and gardening. The kitchen features granite countertops and stainless steel appliances, perfect for preparing meals for your family. 

The Enchanted Forest neighborhood is surrounded by lush greenery, offering winding paths and a sense of magic that aligns with your desire for a quiet and peaceful environment. You'll have easy access to hiking trails, parks, and a strong community spirit. Local cafes and shops are just a short distance away, providing convenient shopping options. 

This neighborhood strikes the perfect balance between nature and convenience, offering a serene escape while still being close to urban amenities like restaurants and theaters. With easy access to reliable bus lines, proximity to major highways, and bike-friendly roads, you'll have no trouble getting around. Don't miss out on the opportunity to call the Enchanted Forest neighborhood your new home.

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

Description: Welcome to Sunset Heights, a prestigious neighborhood offering panoramic views of the city and mountains. This luxurious 5 bedroom, 4 bathroom home in Sunset Heights is perfect for those seeking a comfortable and spacious layout. The gourmet kitchen, formal dining room, and spacious living area provide the perfect setting for entertaining guests. The neighborhood is known for its quiet and family-friendly atmosphere, with top-rated schools, upscale dining options, and convenient shopping nearby. Sunset Heights strikes the perfect balance between suburban tranquility and access to urban amenities, making it an ideal choice for those looking for a peaceful yet vibrant community. Experience the best of luxury living in Sunset Heights.

Property details:
Neighborhood: Sunset Heights
Price: 950000
Bedrooms: 5
Bathrooms: 4
House Size: 3500
Description: Step into luxury in this stunning 5 bedroom, 4 bathroom home in Sunset Heights. The open concept floor plan is perfect for entertaining, with a gourmet kitchen, formal dining room, and a spacious living area. The master suite features a spa-like bathroom and a private balcony with breathtaking views. The backyard oasis includes a pool, hot tub, and outdoor kitchen.
Neighborhood Description: Sunset Heights is a prestigious neighborhood known for its panoramic views of the city and mountains. Residents enjoy easy access to top-rated schools, upscale dining, and shopping. The community is family-friendly with parks, playgrounds, and walking trails. Experience the best of luxury living in Sunset Heights.
======================================


