import os
import re
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from urllib.parse import urlparse
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
def parse_deployment_chat(command_text):
    """
    Function to parse natural language deployment commands and source code location
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Set OpenAI API key
    os.environ["OPENAI_API_KEY"] = api_key

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o"
    )

    # Define prompt template
    template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at interpreting deployment commands.
        Please extract the following information:
        - Deployment platform (str): (e.g. Azure, AWS, GCP) 
        - Application type (str): (e.g. Flask, Django, Node.js)
        - subscription_id (str): Azure subscription ID
        - resource_group_name (str): The name of the resource group
        - location (str): Azure region/location
        - vm_name (str): Name of the Windows VM
        - admin_username (str): Administrator username for the VM
        - admin_password (str): Administrator password for the VM
        
        If it doesn't exist, return None
        Only return the Python dictionary 
        Return the results as a Python dictionary."""),
        ("user", """Please analyze the following deployment command and source code info:
        Command: {text}
        """)
    ])

    # Use RunnableSequence with a single chain
    chain = template | llm

    # Run the chain using invoke
    result = chain.invoke({"text": command_text})

    # Parse the result
    try:
        response_content = result.content  # AIMessage 
        if not response_content.strip():
            raise ValueError("Empty response from the model.")
        print("Raw model response:", response_content)  
        
         # Extract JSON content from response
        json_match = re.search(r"\{.*?\}", response_content, re.DOTALL)  # Match JSON-like block
        if json_match:
            json_data = json_match.group(0)  # Extract matched JSON string
            parsed_data = json.loads(json_data)  # Convert to Python dictionary
            
            # Convert string "None" to Python None
            for key, value in parsed_data.items():
                if value == "None":
                    parsed_data[key] = None
            
            return parsed_data
        else:
            raise ValueError("No JSON content found in the response.")

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response that caused the error:", result.content)
        return {
            "error": "Failed to parse JSON",
            "platform": None,
            "app_type": None,
            "requirements": None,
        }

if __name__ == "__main__":
    sample_command = "Deploy this Flask application on Azure"
    
    result = parse_deployment_chat(sample_command)
    print(result)