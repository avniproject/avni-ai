"""
DSPy Service Layer for Avni Smart Form Builder.

This service provides the API interface for DSPy-powered form analysis,
including configuration, execution, and result formatting for the Avni platform.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

import dspy
from fastapi import HTTPException

from ..dspy_modules import FormImprovementProgram
from ..dspy_modules.simplified_training import (
    train_simplified_analyzer,
    SimplifiedAvniAnalyzer,
    load_trained_model,
    check_trained_model_exists,
)


logger = logging.getLogger(__name__)


class DSPyService:
    """
    Service layer for DSPy-powered form analysis.

    Handles DSPy configuration, model management, and provides
    high-level interfaces for form analysis operations.
    """

    def __init__(self):
        self.form_analyzer: Optional[FormImprovementProgram] = None
        self.avni_analyzer: Optional[SimplifiedAvniAnalyzer] = None
        self.is_configured = False
        self.config = {}
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for DSPy operations."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    async def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Initialize DSPy service with configuration.

        Args:
            config: Optional configuration override

        Returns:
            True if initialization successful
        """
        logger.info("=== DSPy Service Initialization Starting ===")

        try:
            # Load configuration
            logger.info("Loading configuration...")
            self.config = config or self._load_default_config()
            logger.info(f"Configuration loaded: {self.config}")

            # Configure DSPy with language model
            logger.info("Configuring DSPy...")
            await self._configure_dspy()
            logger.info("DSPy configuration completed")

            # Initialize form analyzer
            logger.info("Initializing form analyzer...")
            self.form_analyzer = FormImprovementProgram(
                enable_tracing=self.config.get("enable_tracing", True)
            )
            logger.info("Form analyzer initialized")

            # Load or train Avni-specific analyzer
            model_path = "trained_models/avni_analyzer.pkl"

            if check_trained_model_exists(model_path):
                logger.info("=== Loading Pre-trained Avni Analyzer ===")
                logger.info(f"Loading trained model from {model_path}")
                try:
                    self.avni_analyzer = load_trained_model(model_path)
                    logger.info("✅ Pre-trained Avni analyzer loaded successfully")
                    logger.info(
                        "💡 To retrain models, run: python train_avni_models.py"
                    )
                except Exception as e:
                    logger.error(f"Failed to load pre-trained model: {e}")
                    logger.warning("Falling back to basic analyzer")
                    self.avni_analyzer = SimplifiedAvniAnalyzer()
            else:
                logger.warning("=== No Pre-trained Model Found ===")
                logger.warning(f"No trained model found at {model_path}")
                logger.info("💡 To train models, run: python train_avni_models.py")

                if self.config.get("enable_fallback_training", False):
                    logger.info("Fallback training enabled - training now...")
                    training_config = {
                        "model": self.config.get("model_name", "gpt-4o-mini"),
                        "num_threads": self.config.get("num_threads", 1),
                        "max_bootstrapped_demos": 3,
                        "max_labeled_demos": 5,
                    }
                    try:
                        self.avni_analyzer = await train_simplified_analyzer(
                            training_config
                        )
                        logger.info("Fallback training completed successfully")
                    except Exception as e:
                        logger.error(f"Fallback training failed: {e}")
                        self.avni_analyzer = SimplifiedAvniAnalyzer()
                else:
                    logger.info("Using basic analyzer (no training)")
                    self.avni_analyzer = SimplifiedAvniAnalyzer()

            self.is_configured = True
            logger.info("DSPy service initialized successfully")
            logger.info("=== DSPy Service Initialization Completed ===")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize DSPy service: {e}")
            import traceback

            logger.error(f"Initialization traceback: {traceback.format_exc()}")
            self.is_configured = False
            return False

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default DSPy configuration."""
        return {
            "model_provider": "openai",
            "model_name": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "max_tokens": 4000,
            "temperature": 0.7,
            "enable_tracing": True,
            "cache_enabled": True,
            "timeout_seconds": 300,
        }

    async def _configure_dspy(self):
        """Configure DSPy with the specified language model."""
        try:
            # Configure DSPy language model
            if self.config["model_provider"] == "openai":
                lm = dspy.LM(
                    model=f"openai/{self.config['model_name']}",
                    api_key=self.config["api_key"],
                    max_tokens=self.config["max_tokens"],
                    temperature=self.config["temperature"],
                )
            else:
                raise ValueError(
                    f"Unsupported model provider: {self.config['model_provider']}"
                )

            # Set DSPy configuration
            dspy.configure(lm=lm)

            logger.info(
                f"DSPy configured with {self.config['model_provider']}/{self.config['model_name']}"
            )

        except Exception as e:
            logger.error(f"Failed to configure DSPy: {e}")
            raise

    async def analyze_form(
        self,
        form_json: Dict[str, Any],
        analysis_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a single form using DSPy modules.

        Args:
            form_json: Form configuration as dictionary
            analysis_options: Analysis configuration options

        Returns:
            Comprehensive analysis results
        """
        logger.info("=== DSPy Form Analysis Starting ===")

        if not self.is_configured:
            logger.error("DSPy service not initialized")
            raise HTTPException(status_code=500, detail="DSPy service not initialized")

        try:
            logger.info(
                f"Starting form analysis for: {form_json.get('name', 'Unknown')}"
            )
            logger.info(f"Analysis options: {analysis_options}")

            # Validate input
            logger.info("Validating form input...")
            self._validate_form_input(form_json)
            logger.info("Form input validation passed")

            # Check if form_analyzer is available
            if not self.form_analyzer:
                logger.error("Form analyzer not initialized")
                raise Exception("Form analyzer not initialized")

            logger.info("Calling form_analyzer.forward()...")

            # Perform analysis (tracing handled by DSPy internally in 3.x)
            results = self.form_analyzer.forward(form_json, analysis_options)

            logger.info("Form analyzer completed successfully")
            logger.info(f"Results type: {type(results)}")

            # Post-process results
            logger.info("Post-processing results...")
            logger.info(
                f"Results structure before post-processing: {type(results)} with keys: {list(results.keys()) if isinstance(results, dict) else 'not a dict'}"
            )
            results = self._post_process_results(results, form_json)

            logger.info(
                f"Form analysis completed. Results type: {type(results.get('ranked_recommendations', []))}"
            )
            logger.info("=== DSPy Form Analysis Completed ===")
            return results

        except Exception as e:
            logger.error(f"Form analysis failed: {e}")
            logger.error(f"Exception type: {type(e)}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    async def analyze_multiple_forms(
        self, forms: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze multiple forms concurrently.

        Args:
            forms: List of form configurations

        Returns:
            Batch analysis results
        """
        if not self.is_configured:
            raise HTTPException(status_code=500, detail="DSPy service not initialized")

        try:
            logger.info(f"Starting batch analysis for {len(forms)} forms")

            # Validate inputs
            for i, form in enumerate(forms):
                try:
                    self._validate_form_input(form)
                except Exception as e:
                    logger.warning(f"Skipping invalid form at index {i}: {e}")
                    forms[i] = None

            # Filter out invalid forms
            valid_forms = [f for f in forms if f is not None]

            # Perform batch analysis
            batch_results = await self.form_analyzer.analyze_multiple_forms(valid_forms)

            logger.info(f"Batch analysis completed. Processed {len(valid_forms)} forms")
            return batch_results

        except Exception as e:
            logger.error(f"Batch analysis failed: {e}")
            raise HTTPException(
                status_code=500, detail=f"Batch analysis failed: {str(e)}"
            )

    def _validate_form_input(self, form_json: Dict[str, Any]):
        """Validate form input structure."""
        required_fields = ["name", "formElementGroups"]

        for field in required_fields:
            if field not in form_json:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(form_json["formElementGroups"], list):
            raise ValueError("formElementGroups must be a list")

        if len(form_json["formElementGroups"]) == 0:
            raise ValueError("Form must have at least one element group")

    def _post_process_results(
        self, results: Dict[str, Any], original_form: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Post-process analysis results for API response."""
        # Add form metadata
        results["form_metadata"] = {
            "name": original_form.get("name"),
            "uuid": original_form.get("uuid"),
            "form_type": original_form.get("formType"),
            "total_groups": len(original_form.get("formElementGroups", [])),
            "total_elements": sum(
                len(group.get("formElements", []))
                for group in original_form.get("formElementGroups", [])
            ),
        }

        # Add API response metadata
        results["api_metadata"] = {
            "service_version": "1.0.0",
            "dspy_version": dspy.__version__
            if hasattr(dspy, "__version__")
            else "unknown",
            "processing_timestamp": datetime.now().isoformat(),
        }

        # DSPy now handles structured output directly - minimal post-processing needed
        # Just ensure ranked_recommendations exists
        if "ranked_recommendations" not in results:
            results["ranked_recommendations"] = []

        return results

    async def get_service_status(self) -> Dict[str, Any]:
        """Get DSPy service status and health information."""
        return {
            "service_name": "dspy_form_analyzer",
            "version": "1.0.0",
            "status": "healthy" if self.is_configured else "not_configured",
            "configuration": {
                "model_provider": self.config.get("model_provider"),
                "model_name": self.config.get("model_name"),
                "tracing_enabled": self.config.get("enable_tracing"),
                "cache_enabled": self.config.get("cache_enabled"),
            },
            "capabilities": [
                "form_analysis",
                "field_type_prediction",
                "validation_auditing",
                "suggestion_generation",
                "batch_processing",
            ],
            "timestamp": datetime.now().isoformat(),
        }

    async def optimize_model(
        self, training_data: List[Dict[str, Any]], metric: str = "accuracy"
    ) -> Dict[str, Any]:
        """
        Optimize DSPy modules using training data.

        Args:
            training_data: List of training examples
            metric: Optimization metric

        Returns:
            Optimization results
        """
        if not self.is_configured:
            raise HTTPException(status_code=500, detail="DSPy service not initialized")

        try:
            logger.info(
                f"Starting model optimization with {len(training_data)} examples"
            )

            # This would implement DSPy optimization
            # For now, return placeholder
            return {
                "optimization_status": "not_implemented",
                "message": "Model optimization will be implemented in future versions",
                "training_examples": len(training_data),
                "metric": metric,
            }

        except Exception as e:
            logger.error(f"Model optimization failed: {e}")
            raise HTTPException(
                status_code=500, detail=f"Optimization failed: {str(e)}"
            )

    async def shutdown(self):
        """Shutdown DSPy service and cleanup resources."""
        logger.info("Shutting down DSPy service")
        self.is_configured = False
        self.form_analyzer = None
        self.config = {}


# Global service instance
_dspy_service: Optional[DSPyService] = None


async def get_dspy_service() -> DSPyService:
    """Get or create DSPy service instance."""
    global _dspy_service

    if _dspy_service is None:
        _dspy_service = DSPyService()
        await _dspy_service.initialize()

    return _dspy_service


@asynccontextmanager
async def dspy_service_context():
    """Context manager for DSPy service lifecycle."""
    service = await get_dspy_service()
    try:
        yield service
    finally:
        await service.shutdown()
