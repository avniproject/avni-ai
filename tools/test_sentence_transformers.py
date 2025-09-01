from sentence_transformers import SentenceTransformer, util
import os
import json
from pathlib import Path
from collections import defaultdict

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Load embedding model
model = SentenceTransformer("all-MpNet-base-v2")

# Define app files relative to the tools/apps directory
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
        print(f"Warning: Could not find {name} at {path}")
        continue

if not app_texts:
    raise FileNotFoundError("No app description files found. Please ensure the files exist in the apps/ directory.")

# Precompute embeddings for app descriptions
app_embeddings = {name: model.encode(text, convert_to_tensor=True) for name, text in app_texts.items()}

def match_prompt_to_app(prompt, threshold=0.3):
    # Encode the prompt
    prompt_emb = model.encode(prompt, convert_to_tensor=True)

    # Compute similarities
    scores = {name: float(util.cos_sim(prompt_emb, emb)) for name, emb in app_embeddings.items()}

    # Pick the best
    best_app, best_score = max(scores.items(), key=lambda x: x[1])

    if best_score < threshold:
        return "unmatched", best_score
    return best_app, best_score

def get_expected_app_name(prompt_filename):
    """Convert prompt filename to expected app name.
    e.g., 'cini_prompts.json' -> 'cini'"""
    return prompt_filename.replace('_prompts.json', '')

def process_prompt_files():
    # Find all prompt JSON files
    prompt_files = list((script_dir / "apps").glob("*_prompts.json"))
    if not prompt_files:
        print("No prompt files found in apps/ directory")
        return

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
                    match, score = match_prompt_to_app(prompt)
                    
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
    print(f"📊 SUMMARY: {correct_matches}/{total_prompts} prompts matched correctly ({correct_matches/total_prompts*100:.1f}%)")
    print("="*80)
    
    if mismatches:
        print("\n🔍 MISMATCHES FOUND:")
        for i, m in enumerate(mismatches[:10], 1):  # Show first 10 mismatches
            print(f"\n{i}. File: {m['file']}")
            print(f"   Expected: {m['expected']}")
            print(f"   Matched:  {m['matched']} (score: {m['score']:.2f})")
            print(f"   Prompt:   {m['prompt'][:120]}...")
        
        if len(mismatches) > 10:
            print(f"\n... and {len(mismatches) - 10} more mismatches not shown.")
    
    return mismatches

if __name__ == "__main__":
    process_prompt_files()
# After removing generic prompts-40% threshold:
# SUMMARY: 327/564 prompts matched correctly (58.0%)
# 30% threshold:
# 330/564 prompts matched correctly (58.5%)
# mpnet-base-v2:
#SUMMARY: 323/564 prompts matched correctly (57.3%)


