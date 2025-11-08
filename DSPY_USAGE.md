# DSPy Smart Form Builder for Avni

This document provides comprehensive usage examples for the DSPy-powered Smart Form Builder integrated into the Avni AI server.

## Overview

The DSPy Smart Form Builder provides AI-assisted form creation and validation through the following capabilities:

- **Form Analysis**: Comprehensive analysis of form structure, logic, and content
- **Field Type Prediction**: Intelligent prediction of optimal field types for questions  
- **Validation Auditing**: Detection of structural, logical, and quality issues
- **Smart Suggestions**: Context-aware recommendations for form improvements
- **Batch Processing**: Concurrent analysis of multiple forms

## API Endpoints

All DSPy endpoints are available under the `/dspy` prefix:

### 1. Analyze Single Form

**Endpoint**: `POST /dspy/analyze-form`

Performs comprehensive analysis of a form including type optimization, validation, and suggestions.

**Method 1: Direct Form JSON (Recommended)**
```bash
curl -X POST "http://localhost:8023/dspy/analyze-form?domain=health" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Individual Registration",
    "uuid": "76ab20e6-88c5-413b-ae7b-c58c474e8700",
    "formType": "IndividualProfile", 
    "formElementGroups": [
      {
        "uuid": "061b81bd-a096-4f27-bb6f-b1da97aa8ed7",
        "name": "Basic questions",
        "formElements": [
          {
            "name": "Age",
            "uuid": "37dcbe2b-27be-47a3-a42e-099ac95f1028",
            "concept": {
              "name": "Age",
              "dataType": "Numeric",
              "lowAbsolute": 0.0,
              "highAbsolute": 120.0,
              "unit": "Years"
            }
          }
        ]
      }
    ]
  }'
```

**Method 2: Wrapped Format**
```bash
curl -X POST http://localhost:8023/dspy/analyze-form \
  -H "Content-Type: application/json" \
  -d '{
    "form_json": {
      "name": "Patient Registration", 
      "formElementGroups": [...]
    },
    "domain": "health",
    "analysis_options": {
      "include_type_suggestions": true,
      "include_validation": true,
      "include_suggestions": true
    }
  }'
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "analysis_metadata": {
      "timestamp": "2024-11-07T12:00:00",
      "domain": "health",
      "form_name": "Patient Registration"
    },
    "ranked_recommendations": [
      {
        "type": "field_type_optimization",
        "title": "Optimize field type for 'Age'", 
        "description": "Change from Text to numeric",
        "priority": "medium",
        "rationale": "Age is inherently numeric data",
        "rank": 1
      }
    ],
    "executive_summary": {
      "overview": "Form analysis completed with 3 recommendations",
      "overall_score": 85,
      "recommendation": "minor_enhancements"
    }
  }
}
```

### 2. Batch Analyze Forms

**Endpoint**: `POST /dspy/batch-analyze`

Analyzes multiple forms concurrently for efficiency.

```bash
curl -X POST http://localhost:8023/dspy/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{
    "forms": [
      {
        "name": "Form 1",
        "formElementGroups": [...]
      },
      {
        "name": "Form 2", 
        "formElementGroups": [...]
      }
    ],
    "domain": "health"
  }'
```

### 3. Predict Field Type

**Endpoint**: `POST /dspy/predict-field-type`

Predicts optimal field type for a specific question.

```bash
curl -X POST http://localhost:8023/dspy/predict-field-type \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "What is your marital status?",
    "options": ["Single", "Married", "Divorced", "Widowed"],
    "domain": "health"
  }'
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "question_text": "What is your marital status?",
    "predicted_type": "single_select",
    "confidence": 0.95,
    "rationale": "Fixed set of mutually exclusive options indicates single select",
    "suggestions": [
      "Consider adding 'Prefer not to say' option",
      "Ensure options cover all demographic groups"
    ]
  }
}
```

### 4. Validate Form Structure

**Endpoint**: `POST /dspy/validate-form`

Validates form structure and identifies issues.

```bash
curl -X POST http://localhost:8023/dspy/validate-form \
  -H "Content-Type: application/json" \
  -d '{
    "form_json": {
      "name": "Test Form",
      "formElementGroups": [...]
    }
  }'
```

### 5. Get Domain Insights

**Endpoint**: `GET /dspy/domain-insights?domain=health`

Retrieves domain-specific best practices and insights.

```bash
curl "http://localhost:8023/dspy/domain-insights?domain=health"
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "domain": "health",
    "insights": {
      "critical_fields": ["emergency_contact", "allergies", "current_medications"],
      "best_practices": [
        "Include patient safety fields",
        "Ensure privacy compliance", 
        "Use standardized medical terminology"
      ],
      "common_issues": [
        "Missing emergency contact information",
        "Lack of allergy documentation"
      ]
    }
  }
}
```

### 6. Service Status

**Endpoint**: `GET /dspy/status`

Gets DSPy service health and configuration status.

```bash
curl http://localhost:8023/dspy/status
```

## Integration Examples

### JavaScript/TypeScript Integration

```typescript
class AvniDSPyClient {
  constructor(private baseUrl: string = 'http://localhost:8023') {}

  async analyzeForm(formJson: any, domain = 'health') {
    const response = await fetch(`${this.baseUrl}/dspy/analyze-form`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ form_json: formJson, domain })
    });
    return response.json();
  }

  async predictFieldType(questionText: string, options?: string[], domain = 'health') {
    const response = await fetch(`${this.baseUrl}/dspy/predict-field-type`, {
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_text: questionText, options, domain })
    });
    return response.json();
  }

  async getDomainInsights(domain: string) {
    const response = await fetch(`${this.baseUrl}/dspy/domain-insights?domain=${domain}`);
    return response.json();
  }
}

// Usage example
const client = new AvniDSPyClient();

// Analyze a form
const analysisResult = await client.analyzeForm({
  name: "Patient Intake",
  formElementGroups: [
    // ... form structure
  ]
}, 'health');

console.log(`Form score: ${analysisResult.data.executive_summary.overall_score}`);
console.log(`Recommendations: ${analysisResult.data.ranked_recommendations.length}`);
```

### Python Integration

```python
import requests
import json

class AvniDSPyClient:
    def __init__(self, base_url="http://localhost:8023"):
        self.base_url = base_url
    
    def analyze_form(self, form_json, domain="health", analysis_options=None):
        response = requests.post(
            f"{self.base_url}/dspy/analyze-form",
            json={
                "form_json": form_json,
                "domain": domain,
                "analysis_options": analysis_options
            }
        )
        return response.json()
    
    def predict_field_type(self, question_text, options=None, domain="health"):
        response = requests.post(
            f"{self.base_url}/dspy/predict-field-type",
            json={
                "question_text": question_text,
                "options": options,
                "domain": domain
            }
        )
        return response.json()

# Usage example
client = AvniDSPyClient()

# Predict field type
result = client.predict_field_type(
    "What is your blood type?",
    options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    domain="health"
)

print(f"Predicted type: {result['data']['predicted_type']}")
print(f"Confidence: {result['data']['confidence']}")
```

## Real Form Analysis Example

Here's an example using an actual Avni form structure:

```bash
curl -X POST http://localhost:8023/dspy/analyze-form \
  -H "Content-Type: application/json" \
  -d '{
    "form_json": {
      "name": "Individual Registration",
      "uuid": "c22664a8-81ba-4442-956d-3e812a6d7bca",
      "formType": "IndividualProfile",
      "formElementGroups": [
        {
          "uuid": "b470d24b-c4f4-467b-910b-e0f5fbffb9bb",
          "name": "Details",
          "displayOrder": 1.0,
          "formElements": [
            {
              "name": "Marital status",
              "uuid": "770a06ac-31d5-4bdc-85b4-8daeedcede9e",
              "concept": {
                "name": "Marital status",
                "uuid": "a20a030b-9bef-4ef8-ba8a-88e2b23c1478",
                "dataType": "Coded",
                "answers": [
                  {"name": "Unmarried", "uuid": "65e1cf2b-7e67-4cf7-8360-ab4483a124dc"},
                  {"name": "Divorced", "uuid": "1b152618-fdd8-44d0-8fe0-813015941a59"},
                  {"name": "Separated", "uuid": "5558ecd1-91ab-4d53-aba6-20940862be15"},
                  {"name": "Married", "uuid": "63d6930e-94d0-4797-b780-ce5afbf36494"},
                  {"name": "Widow", "uuid": "b93a8892-7407-4ebb-baf6-f5e6487772ab"}
                ]
              }
            }
          ]
        }
      ]
    },
    "domain": "health"
  }'
```

## Configuration

### Environment Variables

Set these environment variables to configure DSPy:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional DSPy Configuration  
DSPY_MODEL_NAME=gpt-4o-mini          # Default model
DSPY_MAX_TOKENS=4000                 # Max tokens per request
DSPY_TEMPERATURE=0.7                 # Response randomness
DSPY_TRACING=true                    # Enable execution tracing
```

### Domain Support

The system supports different domains with specialized knowledge:

- **health**: Medical forms, patient data, clinical workflows
- **education**: Student information, academic tracking, learning assessments  
- **survey**: Research surveys, questionnaires, data collection

Each domain provides tailored suggestions and validates against domain-specific best practices.

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Description of what went wrong",
  "error_type": "ValueError"
}
```

Common error scenarios:
- Invalid JSON in request body (400)
- Missing required fields (400) 
- DSPy service not configured (500)
- OpenAI API errors (500)

## Performance Considerations

- Single form analysis typically takes 3-10 seconds
- Batch analysis processes forms concurrently for efficiency
- Results can be cached to avoid reanalysis of unchanged forms
- Enable tracing for debugging but disable in production for performance

## Next Steps

1. **Install Dependencies**: Add `dspy-ai>=3.0.3` to your environment
2. **Configure API Keys**: Set up OpenAI API access
3. **Test Endpoints**: Try the example requests above
4. **Integration**: Integrate with your Avni form builder UI
5. **Customization**: Extend modules for organization-specific requirements

## Support

For issues or questions:
- Check logs: `sudo journalctl -u avni-ai -f`  
- Service status: `GET /dspy/status`
- Configuration validation: Check environment variables