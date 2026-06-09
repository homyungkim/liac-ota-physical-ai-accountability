"""Basic tests for the LIAC reference implementation."""

from liac.evidence import (
    event_triggered_sdi_record_generation,
    lifecycle_evidence_chaining,
    verify_chain,
)


def test_sdi_not_emitted_when_installation_integrity_fails():
    sdi, record = event_triggered_sdi_record_generation(
        installation_integrity=0,
        behavior={"semantic_safe": False, "deviation": 1.0},
        context={"environment": "test"},
        threshold=0.5,
        corr_id="test",
    )
    assert sdi == 0
    assert record is None


def test_sdi_emitted_for_unsafe_behavior_above_threshold():
    sdi, record = event_triggered_sdi_record_generation(
        installation_integrity=1,
        behavior={"semantic_safe": False, "deviation": 0.8},
        context={"environment": "test"},
        threshold=0.5,
        corr_id="test",
    )
    assert sdi == 1
    assert record is not None
    assert record["corr_id"] == "test"


def test_lifecycle_chain_verifies():
    lir, chain = lifecycle_evidence_chaining(
        artifact={"name": "demo", "version": "1.0"},
        manifest={"release_id": "r1"},
        target_device={"verification_succeeds": True},
        execution_events=[
            {
                "behavior": {"semantic_safe": False, "deviation": 0.8},
                "context": {"environment": "test"},
            }
        ],
        corr_id="test-chain",
    )
    assert lir["status"] == "complete"
    assert verify_chain(chain)
