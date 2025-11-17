# DSPy Training for Avni Form Analysis

This directory contains the DSPy training system for optimizing prompts for Avni form analysis.

## Overview

The training system uses DSPy's MIPROv2 to optimize prompts for two main tasks:
1. **Issue Identification** - Finding problems in form structures
2. **Suggestion Generation** - Creating improvement recommendations

## Files

- `training.py` - Main training script with CLI interface
- `issue_identifier.py` - DSPy module for identifying form issues
- `suggestion_generator.py` - DSPy module for generating suggestions

## Usage

### Prerequisites

1. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_key_here
   # or add to .env file: OPENAI_API_KEY=your_key_here
   ```

### Training

Run training from the project root:

```bash
# Basic training
uv run python src/dspy/training.py

# Custom options
uv run python src/dspy/training.py --steps 10 --model gpt-4o --force

# Test imports only
uv run python src/dspy/training.py --test-imports
```

### Options

- `--steps N` - Number of training steps (default: 5)
- `--model MODEL` - OpenAI model to use (default: gpt-4o-mini)  
- `--force` - Force retrain even if model exists
- `--test-imports` - Test imports without training

### Output

Trained models are saved to `trained_models/avni_analyzer.pkl` in the project root.

## Training Process

1. Creates training examples for issue identification and suggestion generation
2. Uses DSPy's MIPROv2 optimizer to find optimal prompts
3. Saves the optimized model for later use
4. The trained model contains optimized prompts, not inference logic

## Purpose

This training system is used solely to optimize prompts. The actual form analysis in production uses the optimized prompts directly, not DSPy inference.