#!/usr/bin/env python3
"""
Simplified training script for Avni DSPy models.

Run this directly from the avni-ai directory.
"""

import asyncio
import argparse
import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main training function."""
    
    parser = argparse.ArgumentParser(description='Train Avni DSPy models')
    parser.add_argument('--steps', type=int, default=5, help='Number of training steps')
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help='OpenAI model')
    parser.add_argument('--force', action='store_true', help='Force retrain')
    parser.add_argument('--test-imports', action='store_true', help='Test imports only')
    args = parser.parse_args()
    
    # Load environment directly (avoid complex import chains)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("✅ Environment loaded using dotenv")
        
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment or .env file")
            
        logger.info(f"✅ OpenAI API key found: {OPENAI_API_KEY[:10]}...")
        
    except Exception as e:
        logger.error("❌ Failed to load environment!")
        logger.error(f"Error: {e}")
        logger.error("Solutions:")
        logger.error("1. Add OPENAI_API_KEY=your_key to .env file")
        logger.error("2. Or export OPENAI_API_KEY=your_key_here")
        logger.info("For testing imports only, you can run: python train_models.py --test-imports")
        if '--test-imports' not in sys.argv:
            return
    
    try:
        # Import directly without path manipulation
        import dspy
        logger.info("✅ DSPy available")
        
        # Configure DSPy (skip if testing imports only)
        if not args.test_imports:
            lm = dspy.LM(
                model=f"openai/{args.model}",
                api_key=OPENAI_API_KEY,
                max_tokens=4000,
                temperature=0.7
            )
            dspy.configure(lm=lm)
            logger.info(f"✅ DSPy configured with {args.model}")
        
        # Add src to path for imports
        src_path = Path(__file__).parent / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        # Import simplified training modules
        from dspy_modules.simplified_training import train_simplified_analyzer, save_trained_model
        logger.info("✅ Training modules imported successfully")
        
        if args.test_imports:
            logger.info("✅ All imports successful! You can now train with a real API key.")
            return
        
        logger.info("🚀 Starting training...")
        
        # Training config
        config = {
            "model": args.model,
            "num_threads": 1,
            "max_bootstrapped_demos": 5,
            "max_labeled_demos": 8,
            "training_steps": args.steps
        }
        
        # Create output directory
        output_dir = Path("trained_models")
        output_dir.mkdir(exist_ok=True)
        model_path = output_dir / "avni_analyzer.pkl"
        
        # Check if model exists
        if model_path.exists() and not args.force:
            logger.info(f"✅ Model already exists at {model_path}")
            logger.info("Use --force to retrain")
            return
        
        # Train the simplified model
        logger.info(f"Training with config: {config}")
        trained_analyzer = await train_simplified_analyzer(config)
        
        # Save the model
        save_trained_model(trained_analyzer, str(model_path))
        
        logger.info("✅ Training completed!")
        logger.info(f"📁 Model saved to: {model_path}")
        logger.info("🚀 You can now start the server!")
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        logger.error("Make sure you're running this from the avni-ai directory")
        logger.error("Try: uv run python train_models.py")
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())