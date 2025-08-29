import os
import json
import numpy as np
from pathlib import Path
from openai import OpenAI
from typing import Dict, List, Tuple

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Initialize OpenAI client
openai_client = OpenAI()

def get_expected_app_name(prompt_filename: str) -> str:
    """Convert prompt filename to expected app name.
    e.g., 'cini_prompts.json' -> 'cini'"""
    return prompt_filename.replace('_prompts.json', '')


"""Load app description files from the apps directory."""
app_files = {
    "teach": script_dir / "apps" / "teach.md",
    "phulwari": script_dir / "apps" / "phulwari.md",
    "cini": script_dir / "apps" / "cini.md",
    "sickle_cell": script_dir / "apps" / "sickle_cell_screening.md",
    "gst": script_dir / "apps" / "gst.md",
    "waste_management": script_dir / "apps" / "waste_management.md",
    "social_security": script_dir / "apps" / "social_security.md",
    "waterbody": script_dir / "apps" / "waterbody_desilting.md"
}

# Load app texts with error handling
app_texts = {}
for name, path in app_files.items():
    try:
        app_texts[name] = path.resolve().read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Warning: Could not find {path}")

if not app_texts:
    raise FileNotFoundError("No app description files found. Please ensure the files exist in the apps/ directory.")
    
batch_size = 5
all_embeddings = []

app_descriptions = list(app_texts.values())
batch_size = 5
all_embeddings = []

for i in range(0, len(app_descriptions), batch_size):
    batch = app_descriptions[i:i + batch_size]
    response = openai_client.embeddings.create(
        input=batch,
        model="text-embedding-3-small"
    )
    batch_embeddings = [data.embedding for data in response.data]
    all_embeddings.extend(batch_embeddings)
    

def get_openai_embeddings(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    """Get embeddings for a list of texts using OpenAI's API."""
    # Batch process if more than 5 texts
    response = openai_client.embeddings.create(
        input=text,
        model=model
    )
    batch_embeddings = response.data[0].embedding
    return batch_embeddings

def match_prompt_to_app(prompt: str, app_descriptions: Dict[str, str], threshold: float = 0.5) -> Tuple[str, float]:
    """
    Match a prompt to the most similar app using OpenAI's embeddings.
    
    Args:
        prompt: The input prompt to match
        app_descriptions: Dictionary of app names to their descriptions
        threshold: Similarity threshold (0-1)
        
    Returns:
        A tuple of (best_match_app, best_score) or ("none", best_score) if below threshold
    """
    try: 
        # Calculate cosine similarities
        prompt_emb = get_openai_embeddings(prompt)
        app_embs = all_embeddings
        # Calculate cosine similarity
        similarities = {}
        for (app_name, _), app_emb in zip(app_descriptions.items(), app_embs):
            # Calculate cosine similarity
            similarity = np.dot(prompt_emb, app_emb) / (np.linalg.norm(prompt_emb) * np.linalg.norm(app_emb))
            similarities[app_name] = similarity
        
        # Get best match
        best_app, best_score = max(similarities.items(), key=lambda x: x[1])
        
        if best_score < threshold:
            return "unmatched", best_score
        return best_app, best_score
        
    except Exception as e:
        print(f"Error in OpenAI embedding: {str(e)}")
        return "error", 0.0

def process_prompt_files() -> List[dict]:
    """Process prompt files using OpenAI's text-embedding-3-small model."""
    # Find all prompt JSON files
    prompt_files = list((script_dir / "apps").glob("*_prompts.json"))
    if not prompt_files:
        print("No prompt files found in apps/ directory")
        return []

    # Track mismatches
    mismatches = []
    total_prompts = 0
    correct_matches = 0
    
    # Process each prompt file
    for prompt_file in prompt_files:
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                prompts = data.get('prompts', [])
                expected_app = get_expected_app_name(prompt_file.name)
                
                print(f"\n{'='*80}\nProcessing {len(prompts)} prompts from: {prompt_file.name} (expected app: {expected_app})\n{'='*80}")
                
                file_mismatches = 0
                
                for i, prompt in enumerate(prompts, 1):
                    total_prompts += 1
                    match, score = match_prompt_to_app(prompt, app_texts)
                    
                    if match != expected_app:
                        mismatches.append({
                            'file': prompt_file.name,
                            'prompt': prompt,
                            'expected': expected_app,
                            'matched': match,
                            'score': score
                        })
                        file_mismatches += 1
                        print(f"❌ [{i}] Expected: {expected_app}, Got: {match} (score: {score:.2f})")
                        print(f"   Prompt: {prompt[:120]}...")
                    else:
                        correct_matches += 1
                        print(f"✅ [{i}] Correct match: {match} (score: {score:.2f})")
                
                print(f"\n📊 {file_mismatches}/{len(prompts)} mismatches in {prompt_file.name}")
                        
        except Exception as e:
            print(f"Error processing {prompt_file}: {str(e)}")
    
    # Print summary
    print("\n" + "="*80)
    print(f"📊 OPENAI SUMMARY: {correct_matches}/{total_prompts} prompts matched correctly ({correct_matches/total_prompts*100:.1f}%)")
    print("="*80)
    
    if mismatches:
        print("\n🔍 MISMATCHES FOUND:")
        for i, m in enumerate(mismatches[:10], 1):
            print(f"\n{i}. File: {m['file']}")
            print(f"   Expected: {m['expected']}")
            print(f"   Matched:  {m['matched']} (score: {m['score']:.2f})")
            print(f"   Prompt:   {m['prompt'][:120]}...")
        
        if len(mismatches) > 10:
            print(f"\n... and {len(mismatches) - 10} more mismatches not shown.")
    
    return mismatches

if __name__ == "__main__":
    print("\n" + "="*50 + "\nRunning tests with OpenAI Embeddings\n" + "="*50)
    process_prompt_files()
# 241/607 prompts matched correctly (39.7%)
# After removing generic prompts:
# 231/570 prompts matched correctly (40.5%)