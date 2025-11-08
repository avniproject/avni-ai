# Avni DSPy Model Training

This document explains how to train and use Avni's DSPy models for intelligent form analysis.

## Quick Start

### 1. Train Models (Run Once)

```bash
# Basic training with default settings (5 steps)
uv run python train_models.py

# Advanced training with custom settings
uv run python train_models.py --steps 10 --model gpt-4o
```

### 2. Start Server (Uses Pre-trained Models)

```bash
uv run avni-mcp-server
```

The server will automatically load pre-trained models and start fast!

## Training Options

| Option | Default | Description |
|--------|---------|-------------|
| `--steps` | 5 | Number of MIPROv2 optimization steps |
| `--model` | gpt-4o-mini | OpenAI model (gpt-4o-mini, gpt-4o, gpt-3.5-turbo) |
| `--max-demos` | 8 | Maximum labeled examples for training |
| `--bootstrapped-demos` | 5 | Maximum bootstrapped examples |
| `--output-dir` | trained_models | Directory to save models |
| `--force` | false | Force retrain even if models exist |

## Training Examples

```bash
# Quick training for development
uv run python train_models.py --steps 3

# Production training with better model
uv run python train_models.py --steps 10 --model gpt-4o

# Force retrain existing models
uv run python train_models.py --force

# Test imports without API key
uv run python train_models.py --test-imports
```

## What Gets Trained

The training creates an optimized **AvniFormAnalyzer** that learns to:

1. **Identify Critical Issues**: Name fields in registration forms (system auto-handles)
2. **Detect Type Mismatches**: Age as Text → should be Numeric with bounds
3. **Find Validation Problems**: Phone fields without regex validation
4. **Suggest Improvements**: Missing emergency contacts, voided field cleanup

## Training Process

1. **Creates Examples**: 14 carefully crafted Avni-specific training examples
2. **Sets Instructions**: Detailed prompts with Avni rules and output formats
3. **Runs MIPROv2**: DSPy's optimization algorithm improves prompts and examples
4. **Saves Models**: Persists trained analyzers to `trained_models/` directory

## Output

After training, you'll have:

```
trained_models/
├── avni_analyzer.pkl           # Trained model file
└── training_metadata.json     # Training info and metrics
```

## Server Behavior

- ✅ **With trained models**: Server starts instantly, loads pre-trained analyzers
- ⚠️ **Without trained models**: Server shows warning, uses basic analyzer
- 🔄 **Fallback training**: Enable with `enable_fallback_training=true` in config

## Training Logs

The training shows detailed progress:

```
🚀 Starting Avni model training...
=== Training Examples Overview ===
Example 1: Input fields: ['question_text', 'options', 'context']
=== MIPROv2 Optimization ===
Training Config: {'model': 'gpt-4o-mini', 'steps': 5}
=== Scoring Example ===
Expected: dataType: Numeric; avni_issues: HIGH
Final Score: 0.8
✅ Model saved using pickle to trained_models/avni_analyzer.pkl
```

## Performance

- **Training Time**: ~2-3 minutes for 5 steps
- **Model Size**: ~50KB (lightweight)
- **Server Startup**: <1 second with pre-trained models vs 2-3 minutes with training
- **Analysis Quality**: 73%+ accuracy on validation set

## Troubleshooting

### No OpenAI API Key
```
OPENAI_API_KEY environment variable not set!
export OPENAI_API_KEY=your_key_here
```

### Training Failed
- Check API key and internet connection
- Reduce steps: `--steps 3`
- Use smaller model: `--model gpt-3.5-turbo`

### Server Can't Find Models
```
No trained model found at trained_models/avni_analyzer.pkl
💡 To train models, run: python train_avni_models.py
```

### Force Retrain
```bash
uv run python train_avni_models.py --force
```

## Development Workflow

1. **Initial Setup**: `uv run python train_avni_models.py`
2. **Development**: Start server, models load instantly
3. **Improve Training**: Add examples, retrain with `--force`
4. **Production**: Use `--steps 10 --model gpt-4o` for best quality

The trained models are portable - you can copy `trained_models/` between environments!