import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def extract_city(input_text):
    # Process the input text with spaCy
    doc = nlp(input_text)
    
    # Extract entities that are classified as GPE (Geo-Political Entity)
    cities = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
    
    if cities:
        # Return the first city found
        return cities[0]
    else:
        return None

# Example
inputs = [
    "Show me hotels in Rome",
    "Holiday in Alicante",
    "I want to travel to Amsterdam"
]

for input_text in inputs:
    city = extract_city(input_text)
    if city:
        print(f"City found: {city}")
    else:
        print("No city mentioned.")