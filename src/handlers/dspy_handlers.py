"""
DSPy request handlers for Avni Smart Form Builder endpoints.
"""

import logging
import json
from typing import Dict, Any, Optional
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.dspy_service import get_dspy_service
from ..dspy_modules.simplified_training import train_simplified_analyzer


logger = logging.getLogger(__name__)


async def analyze_form_request(request: Request) -> JSONResponse:
    """
    Handle form analysis requests.
    
    Expected JSON payload can be either:
    1. Direct form JSON: {"name": "...", "formElementGroups": [...], ...}
    2. Wrapped format: {"form_json": {...}, "analysis_options": {...}}
    """
    try:
        # Parse request body
        body = await request.json()
        
        # Check if this is a direct form JSON or wrapped format
        if "formElementGroups" in body:
            # Direct form JSON format
            form_json = body
            analysis_options = None
        else:
            # Wrapped format
            form_json = body.get("form_json")
            analysis_options = body.get("analysis_options")
        
        # Validate required fields
        if not form_json:
            return JSONResponse(
                {"error": "form_json is required or invalid form structure"}, 
                status_code=400
            )
        
        # Get DSPy service
        dspy_service = await get_dspy_service()
        
        # Perform analysis
        results = await dspy_service.analyze_form(
            form_json=form_json,
            analysis_options=analysis_options
        )
        
        return JSONResponse({
            "success": True,
            "data": results
        })
        
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Invalid JSON in request body"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Form analysis failed: {e}")
        return JSONResponse(
            {"error": f"Analysis failed: {str(e)}"},
            status_code=500
        )


async def batch_analyze_forms_request(request: Request) -> JSONResponse:
    """
    Handle batch form analysis requests.
    
    Expected JSON payload:
    {
        "forms": [{...}, {...}]
    }
    """
    try:
        # Parse request body
        body = await request.json()
        forms = body.get("forms")
        
        # Validate required fields
        if not forms or not isinstance(forms, list):
            return JSONResponse(
                {"error": "forms must be a non-empty list"},
                status_code=400
            )
        
        # Get DSPy service
        dspy_service = await get_dspy_service()
        
        # Perform batch analysis
        results = await dspy_service.analyze_multiple_forms(
            forms=forms
        )
        
        return JSONResponse({
            "success": True,
            "data": results
        })
        
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Invalid JSON in request body"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        return JSONResponse(
            {"error": f"Batch analysis failed: {str(e)}"},
            status_code=500
        )


async def predict_field_type_request(request: Request) -> JSONResponse:
    """
    Handle field type prediction requests.
    
    Expected JSON payload:
    {
        "question_text": "What is your age?",
        "options": ["18-25", "26-35", "36-45"]
    }
    """
    try:
        # Parse request body
        body = await request.json()
        question_text = body.get("question_text")
        options = body.get("options")
        
        # Validate required fields
        if not question_text:
            return JSONResponse(
                {"error": "question_text is required"},
                status_code=400
            )
        
        # Get DSPy service
        dspy_service = await get_dspy_service()
        
        # Create minimal form for analysis
        test_form = {
            "name": "Field Type Test",
            "formElementGroups": [{
                "name": "Test Group",
                "formElements": [{
                    "name": question_text,
                    "concept": {
                        "dataType": "Text",
                        "answers": [{"name": opt} for opt in (options or [])]
                    }
                }]
            }]
        }
        
        # Analyze form to get type prediction
        results = await dspy_service.analyze_form(
            form_json=test_form,
            analysis_options={
                "include_validation": False,
                "include_suggestions": False
            }
        )
        
        # Extract type prediction
        type_analysis = results.get("component_results", {}).get("type_analysis", {})
        predictions = type_analysis.get("predictions", [])
        
        if predictions:
            prediction = predictions[0]
            return JSONResponse({
                "success": True,
                "data": {
                    "question_text": question_text,
                    "predicted_type": prediction.get("field_type"),
                    "confidence": prediction.get("confidence"),
                    "rationale": prediction.get("rationale"),
                    "suggestions": prediction.get("suggestions", []),
                    "current_type": "Text"
                }
            })
        else:
            return JSONResponse({
                "success": False,
                "error": "No type prediction generated"
            })
        
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Invalid JSON in request body"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Field type prediction failed: {e}")
        return JSONResponse(
            {"error": f"Prediction failed: {str(e)}"},
            status_code=500
        )


async def validate_form_structure_request(request: Request) -> JSONResponse:
    """
    Handle form validation requests.
    
    Expected JSON payload:
    {
        "form_json": {...}
    }
    """
    try:
        # Parse request body
        body = await request.json()
        form_json = body.get("form_json")
        
        # Validate required fields
        if not form_json:
            return JSONResponse(
                {"error": "form_json is required"},
                status_code=400
            )
        
        # Get DSPy service
        dspy_service = await get_dspy_service()
        
        # Analyze form with focus on validation
        results = await dspy_service.analyze_form(
            form_json=form_json,
            analysis_options={
                "include_type_suggestions": False,
                "include_suggestions": False,
                "include_validation": True
            }
        )
        
        # Extract validation results
        validation_results = results.get("component_results", {}).get("validation", {})
        issues = validation_results.get("issues", [])
        
        return JSONResponse({
            "success": True,
            "data": {
                "form_name": form_json.get("name"),
                "validation_summary": validation_results.get("summary", {}),
                "issues": issues,
                "recommendations": validation_results.get("recommendations", []),
                "overall_score": validation_results.get("summary", {}).get("overall_score", 0)
            }
        })
        
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Invalid JSON in request body"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Form validation failed: {e}")
        return JSONResponse(
            {"error": f"Validation failed: {str(e)}"},
            status_code=500
        )




async def get_dspy_service_status_request(request: Request) -> JSONResponse:
    """Handle DSPy service status requests."""
    try:
        # Get DSPy service
        dspy_service = await get_dspy_service()
        
        # Get service status
        status = await dspy_service.get_service_status()
        
        return JSONResponse({
            "success": True,
            "data": status
        })
        
    except Exception as e:
        logger.error(f"Failed to get service status: {e}")
        return JSONResponse(
            {"error": f"Status check failed: {str(e)}"},
            status_code=500
        )


async def retrain_avni_analyzer_request(request: Request) -> JSONResponse:
    """
    Retrain the Avni analyzer with MIPROv2.
    
    Expected JSON payload:
    {
        "training_config": {
            "num_trials": 10,
            "max_bootstrapped_demos": 5,
            "max_labeled_demos": 10
        }
    }
    """
    try:
        # Parse request body
        body = await request.json()
        training_config = body.get("training_config", {})
        
        # Default training configuration
        config = {
            "model": "gpt-4o-mini",
            "num_trials": training_config.get("num_trials", 5),
            "max_bootstrapped_demos": training_config.get("max_bootstrapped_demos", 3),
            "max_labeled_demos": training_config.get("max_labeled_demos", 5)
        }
        
        logger.info(f"Starting Avni analyzer retraining with config: {config}")
        
        # Train the analyzer
        trained_analyzer = await train_simplified_analyzer(config)
        
        # Update the service with new analyzer
        dspy_service = await get_dspy_service()
        dspy_service.avni_analyzer = trained_analyzer
        
        return JSONResponse({
            "success": True,
            "message": "Avni analyzer retrained successfully",
            "training_config": config
        })
        
    except json.JSONDecodeError:
        return JSONResponse({
            "error": "Invalid JSON in request body"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Retraining failed: {e}")
        return JSONResponse({
            "error": f"Retraining failed: {str(e)}"},
            status_code=500
        )