import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

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

def get_expected_app_name(prompt_filename: str) -> str:
    """Convert prompt filename to expected app name."""
    return prompt_filename.replace('_prompts.json', '')

def classify_prompt(prompt: str, categories: Dict[str, str]) -> str:
    """Classify a prompt into one of the app categories using OpenAI."""
    try:
        # Create a system message that explains the task
        system_message = """You are an AI assistant that classifies prompts into specific app categories.
        Choose the most appropriate category based on the prompt's content and intent.
        Respond with ONLY the category name, nothing else."""
        
        # Create the user message with categories and prompt
        categories_text = "\n".join([f"- {name}: {desc}" for name, desc in categories.items()])
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

def process_prompt_files() -> None:
    """Process all prompt files and classify them using OpenAI."""
    script_dir = Path(__file__).parent
    prompt_files = list(script_dir.glob("*_prompts.json"))
    
    if not prompt_files:
        print("No prompt files found in the directory")
        return

    results = []
    total_prompts = 0
    correct_matches = 0
    
    for prompt_file in prompt_files:
        expected_app = get_expected_app_name(prompt_file.name)
        print(f"\nProcessing {prompt_file.name} (expected: {expected_app})")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            prompts = data.get('prompts', [])
            print("number of prompts", len(prompts))
            file_results = []
            for i, prompt in enumerate(prompts, 1):
                total_prompts += 1
                print(f"  Classifying prompt {i}/{len(prompts)}...", end="\r")
                
                predicted = classify_prompt(prompt, APP_CATEGORIES)
                is_correct = predicted == expected_app
                
                if is_correct:
                    correct_matches += 1
                else:
                    print(f"\n❌ Mismatch in {prompt_file.name} prompt {i}")
                    print(f"   Expected: {expected_app}")
                    print(f"   Got:      {predicted}")
                    print(f"   Prompt:   {prompt}")
                    print("-" * 80)

                file_results.append({
                    "prompt": prompt,
                    "expected": expected_app,
                    "predicted": predicted,
                    "correct": is_correct
                })
            
            # Print file summary
            correct = sum(1 for r in file_results if r["correct"])
            print(f"  {correct}/{len(prompts)} correct ({correct/len(prompts)*100:.1f}%)")
            
            results.extend(file_results)
    
    # Print final summary
    print("\n" + "="*50)
    print(f"FINAL RESULTS: {correct_matches}/{total_prompts} correct ({correct_matches/total_prompts*100:.1f}%)")
    
    # Save detailed results
    with open(script_dir / "classification_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    process_prompt_files()


