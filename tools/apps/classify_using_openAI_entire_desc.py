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

def get_expected_app_name(prompt_filename: str) -> str:
    """Convert prompt filename to expected app name."""
    return prompt_filename.replace('_prompts.json', '')

def load_app_descriptions() -> Dict[str, str]:
    """Load full content of app description markdown files."""
    script_dir = Path(__file__).parent
    app_files = {
        "teach": script_dir / "teach.md",
        "phulwari": script_dir / "phulwari.md",
        "cini": script_dir / "cini.md",
        "sickle_cell": script_dir / "sickle_cell_screening.md",
        "gst": script_dir / "gst.md",
        "waste_management": script_dir / "waste_management.md",
        "social_security": script_dir / "social_security.md",
        "waterbody": script_dir / "waterbody_desilting.md"
    }
    
    app_contents = {}
    for name, path in app_files.items():
        try:
            app_contents[name] = path.read_text(encoding='utf-8')
        except FileNotFoundError:
            print(f"Warning: Could not find {path}")
            app_contents[name] = ""
    
    return app_contents

def classify_prompt(prompt: str, app_contents: Dict[str, str]) -> str:
    """Classify a prompt using the full app description content."""
    try:
        # Create a system message that explains the task
        system_message = """You are an AI assistant that classifies prompts into specific app categories.
        Analyze the prompt and the full app descriptions to determine the match.
        Respond with ONLY the app name, nothing else."""
        
        # Format the app descriptions
        apps_text = "\n\n".join([f"===App Name: {app_name} ===\n Description: {content}" 
                               for app_name, content in app_contents.items()])
        
        user_message = f"""App Descriptions:
        {apps_text}

        Prompt to classify: {prompt}

        Respond with ONLY the app name that matches the prompt from the list above.
        If no good match is found, respond with 'unmatched'."""
        
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
        
        # Validate the response is one of our apps
        return category if category in app_contents else "unmatched"
        
    except Exception as e:
        print(f"Error in classification: {str(e)}")
        return "error"

def process_prompt_files() -> None:
    """Process all prompt files and classify them using OpenAI with full descriptions."""
    script_dir = Path(__file__).parent
    prompt_files = list(script_dir.glob("*_prompts.json"))
    
    if not prompt_files:
        print("No prompt files found in the directory")
        return

    # Load all app descriptions once
    app_contents = load_app_descriptions()
    results = []
    total_prompts = 0
    correct_matches = 0
    
    for prompt_file in prompt_files:
        expected_app = get_expected_app_name(prompt_file.name)
        print(f"\nProcessing {prompt_file.name} (expected: {expected_app})")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            prompts = data.get('prompts', [])
            
            file_results = []
            for i, prompt in enumerate(prompts, 1):
                total_prompts += 1
                print(f"  Classifying prompt {i}/{len(prompts)}...", end="\r")
                
                predicted = classify_prompt(prompt, app_contents)
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
            print(f"\n📊 {correct}/{len(prompts)} correct ({correct/len(prompts)*100:.1f}%)")
            
            results.extend(file_results)
    
    # Print final summary
    print("\n" + "="*50)
    print(f"FINAL RESULTS: {correct_matches}/{total_prompts} correct ({correct_matches/total_prompts*100:.1f}%)")
    
    # Save detailed results
    with open(script_dir / "classification_results_full_descriptions.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    process_prompt_files()

### Tested for GST and Phulwari apps
### only around 50% - returned wrongly even for prompt that stated 'app for recording sugar levels'