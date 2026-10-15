from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from .utils import load_yaml
from .steps import STEP_REGISTRY, BaseStep

class PrivacyImpactAssessmentEngine:
    """Engine that loads a YAML workflow definition and executes it.
    The workflow is defined as an ordered list of step identifiers.
    """

    def __init__(self, config_path: str | Path = "src/config.yaml"):
        self.config_path = Path(config_path)
        self.config = load_yaml(self.config_path)
        self.steps: List[BaseStep] = self._build_steps()

    def _build_steps(self) -> List[BaseStep]:
        step_names: List[str] = self.config.get("workflow", [])
        steps: List[BaseStep] = []
        for name in step_names:
            step_cls = STEP_REGISTRY.get(name)
            if not step_cls:
                raise ValueError(f"Unknown step '{name}' in workflow configuration.")
            steps.append(step_cls())
        return steps

    def run(self) -> str:
        """Execute the workflow and return the generated report text.
        Raises:
            RuntimeError: If any step fails unexpectedly.
        """
        context: Dict[str, Any] = {}
        for step in self.steps:
            try:
                step.run(context)
            except Exception as exc:
                raise RuntimeError(f"Step {step.__class__.__name__} failed: {exc}") from exc
        report_text: str = context.get("report_text", "")
        return report_text
