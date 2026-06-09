"""
Demonstration of LIAC lifecycle evidence chaining and SDI record generation.

Run from the repository root:

    python examples/run_demo.py
"""

from pathlib import Path
import json
import sys

# Allow running this example without installing the package.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from liac.evidence import lifecycle_evidence_chaining, verify_chain  # noqa: E402


def main() -> None:
    artifact = {
        "name": "warehouse-robot-perception-planner",
        "version": "1.0.0",
        "provenance": "demo-build-pipeline",
    }

    manifest = {
        "release_id": "ota-release-2026-demo",
        "target": "warehouse-mobile-robot",
        "software_version": "1.0.0",
    }

    target_device = {
        "device_id": "robot-unit-demo-001",
        "deploy_id": "deploy-2026-demo-001",
        "verification_succeeds": True,
        "attestation": "demo-platform-attestation",
    }

    execution_events = [
        {
            "timestamp": "2026-06-09T00:00:00+00:00",
            "behavior": {
                "semantic_safe": True,
                "deviation": 0.0,
                "description": "nominal navigation",
            },
            "context": {
                "environment": "warehouse",
                "lighting": "normal",
                "surface": "dry",
                "sensor_status": "nominal",
                "mode": "autonomous",
            },
        },
        {
            "timestamp": "2026-06-09T00:05:00+00:00",
            "behavior": {
                "semantic_safe": False,
                "deviation": 0.82,
                "description": "navigation instability near reflective wet flooring",
            },
            "context": {
                "environment": "warehouse",
                "lighting": "abnormal",
                "surface": "reflective-wet-floor",
                "sensor_status": "perturbed",
                "mode": "autonomous",
            },
        },
    ]

    lir, chain = lifecycle_evidence_chaining(
        artifact=artifact,
        manifest=manifest,
        target_device=target_device,
        execution_events=execution_events,
        threshold=0.5,
        corr_id="demo-correlation-id",
    )

    print("Lifecycle Integrity Record:")
    print(json.dumps(lir, indent=2))

    print("\nEvidence Chain:")
    print(json.dumps(chain, indent=2))

    print("\nChain verification:", verify_chain(chain))


if __name__ == "__main__":
    main()
