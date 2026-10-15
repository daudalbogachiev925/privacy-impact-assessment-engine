# Privacy Impact Assessment Workflow Engine

This repository provides a lightweight, extensible engine for running Privacy Impact Assessments (PIA). The engine loads a YAML configuration that defines the workflow steps, executes them in order, and produces a human‑readable report.

## Features
- Declarative workflow definition via `config.yaml`
- Strong data validation using **pydantic**
- Pluggable step architecture (collect data, evaluate risk, generate report, etc.)
- Full test suite with **pytest**

## Installation
```bash
git clone https://github.com/yourusername/privacy-impact-assessment-engine.git
cd privacy-impact-assessment-engine
python -m venv .venv
source .venv/bin/activate  # on Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```python
from src.engine import PrivacyImpactAssessmentEngine

engine = PrivacyImpactAssessmentEngine(config_path='src/config.yaml')
report = engine.run()
print(report)
```

## Running Tests
```bash
pytest -q
```

## Extending the Engine
Add new step classes in `src/steps.py` that inherit from `BaseStep` and register them in the `STEP_REGISTRY` dictionary. Then reference the step name in `config.yaml`.
