from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any, List

from .models import DataAsset, Impact, AssessmentReport
from .validators import validate_sensitivity

class BaseStep(ABC):
    """Abstract base class for all workflow steps."""

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> None:
        """Execute the step, mutating the shared `context` dict.
        Args:
            context: A mutable dictionary shared across steps.
        """
        pass

class CollectDataStep(BaseStep):
    """Simulate collection of data assets for the assessment."""

    def run(self, context: Dict[str, Any]) -> None:
        assets = [
            DataAsset(
                name="Customer Database",
                description="Personal data of customers",
                sensitivity="high",
                owner_email="privacy@example.com",
            ),
            DataAsset(
                name="Website Analytics",
                description="Aggregated usage statistics",
                sensitivity="low",
                owner_email="analytics@example.com",
            ),
        ]
        context["assets"] = assets

class RiskEvaluationStep(BaseStep):
    """Calculate a simple risk score for each asset based on sensitivity.
    The scoring model is illustrative only.
    """

    SENSITIVITY_WEIGHT = {"low": 10, "medium": 50, "high": 90}

    def run(self, context: Dict[str, Any]) -> None:
        assets: List[DataAsset] = context.get("assets", [])
        impacts: List[Impact] = []
        for asset in assets:
            weight = self.SENSITIVITY_WEIGHT[validate_sensitivity(asset.sensitivity)]
            # Simple deterministic score: weight + 5 for demonstration
            score = min(100, weight + 5)
            impacts.append(
                Impact(
                    asset=asset,
                    risk_score=score,
                    justification=f"Risk derived from sensitivity '{asset.sensitivity}'.",
                )
            )
        context["impacts"] = impacts

class ReportGenerationStep(BaseStep):
    """Generate a textual report from the calculated impacts."""

    def run(self, context: Dict[str, Any]) -> None:
        impacts: List[Impact] = context.get("impacts", [])
        lines = ["Privacy Impact Assessment Report", "=" * 35, ""]
        for imp in impacts:
            lines.append(f"Asset: {imp.asset.name}")
            lines.append(f"  Description : {imp.asset.description}")
            lines.append(f"  Sensitivity : {imp.asset.sensitivity}")
            lines.append(f"  Owner Email : {imp.asset.owner_email}")
            lines.append(f"  Risk Score  : {imp.risk_score}")
            lines.append(f"  Justification: {imp.justification}")
            lines.append("")
        summary = f"Overall, {len(impacts)} assets were evaluated."
        report = AssessmentReport(impacts=impacts, summary=summary)
        context["report"] = report
        context["report_text"] = "\n".join(lines) + "\n" + summary

# Registry mapping step names (as they appear in config) to classes
STEP_REGISTRY = {
    "collect_data": CollectDataStep,
    "evaluate_risk": RiskEvaluationStep,
    "generate_report": ReportGenerationStep,
}
