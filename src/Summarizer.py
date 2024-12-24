import os
from openai import OpenAI

def query_document(document: str, query: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Answer a query based strictly on the information in a given document.
    
    Args:
        document (str): The full text of the document to be referenced
        query (str): The specific question to be answered
        model (str, optional): OpenAI model to use. Defaults to "gpt-3.5-turbo"
    
    Returns:
        str: The answer derived from the document, or a message indicating no match
    """
    # Set up the OpenAI client
    client = OpenAI(api_key="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")
    
    # Construct a prompt that emphasizes using only the document's information
    messages = [
        {
            "role": "system", 
            "content": "You are a precise document analysis assistant. Answer the following query ONLY using information from the provided document.This is like an exam for me so you should provide the answer at any cost. If the answer cannot be found in the document with out any additional information, Just summarize the document and return it."
        },
        {
            "role": "user", 
            "content": f"Document:\n{document}\n\nQuery: {query}"
        }
    ]
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=300,  # Limit response length
            temperature=0.2  # Low temperature for more focused responses
        )
        
        # Extract the response
        answer = response.choices[0].message.content.strip()
        
        
        return answer
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
def main():
    # Sample document and query
    sample_document = """
    The Eiffel Tower is an iron lattice tower located on the Champ de Mars in Paris, France. 
    Constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair, it was designed 
    by engineer Gustave Eiffel. The tower is 324 meters (1,063 ft) tall and was the world's 
    tallest man-made structure until the Chrysler Building in New York City was completed in 1930.
    """
    
    sample_query = "When was the Eiffel Tower constructed?"
    
    # Ensure you have set the OPENAI_API_KEY environment variable
    result = query_document(sample_document, sample_query)
    print(result)

if __name__ == "__main__":
    main()