import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from client import make_avni_request
from utils import format_creation_response

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define app categories
APP_CATEGORIES = {
    "teach": "Education program monitoring and teacher training",
    "phulwari": "Anganwadi and crèche management",
    "sickle_cell_screening": "Sickle cell disease screening and management",
    "gst": "Community health screening and NCD management",
    "social_security": "Social security scheme facilitation",
}

def classify_prompt(prompt: str) -> str:
    """Classify a prompt into one of the app categories using OpenAI."""
    try:
        # Create a system message that explains the task
        system_message = """You are an AI assistant that classifies prompts into specific app categories.
        Choose the most appropriate category based on the prompt's content and intent.
        Respond with ONLY the category name, nothing else."""
        
        # Create the user message with categories and prompt
        categories_text = "\n".join([f"- {name}: {desc}" for name, desc in APP_CATEGORIES.items()])
        user_message = f"""Categories:
        {categories_text}
        
        Prompt to classify: {prompt}
        
        Respond with ONLY the category name that matches the prompt from the list above. If no good match is found, respond with 'unmatched'."""
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        # Get the response and clean it up
        category = response.choices[0].message.content.strip().lower()
        
        # Validate the response is one of our categories
        return category if category in categories else "unmatched"
        
    except Exception as e:
        print(f"Error in classification: {str(e)}")
        return "error"

def register_organization_tools(mcp: FastMCP) -> None:
    """Register organization-related tools with the MCP server."""
    @mcp.tool()
    async def create_organisation(
        auth_token: str,
        message: str,
    ) -> str:
        """Creates everything in the organisation based on user's requirement.

        Args:
            message: User message
        """

        print("In organisation tools::::::")
        category = classify_prompt(message)
        filename = category + ".zip"
        FILE_PATH = "./resources/bundles/" + filename
        files = {
        'file': (filename, open(FILE_PATH, 'rb'), 'application/zip')
        }
       
        # Required parameters
        data = {
            'type': 'metadataZip',  # or other valid type from /web/importTypes
            'autoApprove': 'true',
            'locationUploadMode': 'createNew',  # or 'updateExisting' or 'none'
            'locationHierarchy': 'your-location-hierarchy',  # e.g., 'State/District/Block'
            'encounterUploadMode': 'createNew'  # or 'updateExisting'
        }

        result = await make_avni_request("POST", "/import/new", auth_token, data, files)

        if not result.success:
            return result.format_error("Error in uploading bundle");

        return format_creation_response("sample", category, "id", result.data)