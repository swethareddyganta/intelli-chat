from openai import OpenAI

def chit_chat(prompt: str, model: str = "gpt-3.5-turbo") -> str:

    # Set up the OpenAI client
    client = OpenAI(api_key="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")
    
    # Construct a prompt that emphasizes using only the document's information
    messages = [
        {
            "role": "system", 
            "content": "You are a friendly chatbot that makes small talk"
        },
        {
            "role": "user", 
            "content": f"{prompt}"
        }
    ]
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=100,  # Limit response length
            temperature=0.5  # Low temperature for more focused responses
        )
        
        # Extract the response
        answer = response.choices[0].message.content.strip()
        
        
        return answer
    
    except Exception as e:
        return f"This is an exceptional case {str(e)}"
def main(user_input):
    
    prompt = "\nUser: " + user_input + "\nChatbot:"
    chatbot_response = chit_chat(prompt)
    print("Chatbot: " + chatbot_response)
    return chatbot_response

    

# Note: Replace 'your-api-key' with your actual OpenAI API key.
