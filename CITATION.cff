"""
Reference implementation of LIAC lifecycle evidence chaining and SDI emission.

This module corresponds to the algorithmic view in the associated IEEE Access
article. It is intentionally compact and reproducibility-oriented.

It does not implement production-grade secure storage, attestation, trusted
execution, certificate validation, or tamper-resistant logging.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple
from uuid import uuid4


JsonDict = Dict[str, Any]


def utc_now_iso() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def hash_json(value: Any) -> str:
    """
    Compute a stable SHA-256 hash over a JSON-serializable object.

    The object is serialized with sorted keys to make the digest stable across
    Python executions when input values are identical.
    """
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EvidenceRecord:
    """A lightweight lifecycle evidence record."""

    stage: str
    timestamp: str
    corr_id: str
    payload: JsonDict
    prev_hash: Optional[str] = None
    record_hash: Optional[str] = None

    def with_hash(self) -> "EvidenceRecord":
        """Return a copy of this record with its record_hash field populated."""
        unsigned = {
            "stage": self.stage,
            "timestamp": self.timestamp,
            "corr_id": self.corr_id,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
        }
        digest = hash_json(unsigned)
        return EvidenceRecord(
            stage=self.stage,
            timestamp=self.timestamp,
            corr_id=self.corr_id,
            payload=self.payload,
            prev_hash=self.prev_hash,
            record_hash=digest,
        )

    def to_dict(self) -> JsonDict:
        """Convert the record to a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class LifecyclePolicy:
    """
    Minimal evidence policy for demonstration.

    In a deployed system, this policy may include retention rules, storage
    backend selection, cryptographic binding, access control, batching rules,
    and platform attestation requirements.
    """

    protect_records: bool = True
    storage_label: str = "demo-append-only-log"


def protect_store(record: EvidenceRecord, policy: LifecyclePolicy) -> EvidenceRecord:
    """
    Demonstration placeholder for integrity-protected storage.

    The function returns the hashed record. In production, this operation should
    be replaced or extended with secure append-only storage, hardware-backed
    attestation, transparency logging, or another tamper-evident mechanism.
    """
    if not policy.protect_records:
        return record
    return record.with_hash()


def _make_record(
    *,
    stage: str,
    corr_id: str,
    payload: JsonDict,
    prev_hash: Optional[str],
    policy: LifecyclePolicy,
    timestamp: Optional[str] = None,
) -> EvidenceRecord:
    """Create and protect a lifecycle evidence record."""
    record = EvidenceRecord(
        stage=stage,
        timestamp=timestamp or utc_now_iso(),
        corr_id=corr_id,
        payload=payload,
        prev_hash=prev_hash,
    )
    return protect_store(record, policy)


def default_semantic_safety_predicate(behavior: JsonDict) -> bool:
    """
    Example semantic safety predicate.

    The demo treats behavior as semantically safe when the field
    ``semantic_safe`` is explicitly True.
    """
    return bool(behavior.get("semantic_safe", False))


def default_deviation_measure(behavior: JsonDict, safety_set: Any) -> float:
    """
    Example deviation measure.

    The demo expects a numeric field named ``deviation``. If absent, it returns
    0.0 for safe behavior and 1.0 for unsafe behavior.
    """
    if "deviation" in behavior:
        return float(behavior["deviation"])
    return 0.0 if default_semantic_safety_predicate(behavior) else 1.0


def classify_deviation(behavior: JsonDict, context: JsonDict, deviation: float) -> str:
    """
    Example deviation classifier.

    This function intentionally uses a simple rule to keep the reference
    implementation transparent and reproducible.
    """
    if deviation >= 0.9:
        return "critical-semantic-deviation"
    if deviation >= 0.5:
        return "semantic-deviation"
    return "minor-deviation"


def context_summary(context: JsonDict) -> JsonDict:
    """
    Produce a bounded context summary for evidence recording.

    This example preserves only high-level metadata. A real system should define
    a privacy-preserving and deployment-specific context summarization policy.
    """
    allowed_keys = ["environment", "lighting", "surface", "sensor_status", "mode"]
    return {key: context.get(key) for key in allowed_keys if key in context}


def event_triggered_sdi_record_generation(
    *,
    installation_integrity: int,
    behavior: JsonDict,
    safety_predicate: Callable[[JsonDict], bool] = default_semantic_safety_predicate,
    context: Optional[JsonDict] = None,
    deviation_measure: Callable[[JsonDict, Any], float] = default_deviation_measure,
    safety_set: Any = None,
    threshold: float = 0.5,
    corr_id: str,
    timestamp: Optional[str] = None,
) -> Tuple[int, Optional[JsonDict]]:
    """
    Algorithm 2: Event-Triggered SDI Record Generation.

    Parameters mirror the manuscript-level abstraction:

    - installation_integrity: I_SI, installation-time artifact integrity predicate
    - behavior: B_t, runtime behavior at time t
    - safety_predicate: membership check for the semantic safety set
    - context: C_t, runtime context summary
    - deviation_measure: delta(B_t, S_safe)
    - threshold: tau, SDI triggering threshold
    - corr_id: lifecycle correlation identifier

    Returns:
        (SDI_t, R_SDI_t), where SDI_t is 0 or 1 and R_SDI_t is either an
        evidence record dictionary or None.
    """
    if installation_integrity != 1:
        return 0, None

    if safety_predicate(behavior):
        return 0, None

    dev = deviation_measure(behavior, safety_set)
    if dev <= threshold:
        return 0, None

    context = context or {}
    h_context = hash_json(context_summary(context))
    m_cls = classify_deviation(behavior, context, dev)

    record = {
        "stage": "execution",
        "timestamp": timestamp or utc_now_iso(),
        "context_summary_hash": h_context,
        "deviation_class": m_cls,
        "deviation_measure": dev,
        "corr_id": corr_id,
    }
    return 1, record


def lifecycle_evidence_chaining(
    *,
    artifact: JsonDict,
    manifest: JsonDict,
    target_device: JsonDict,
    execution_events: Sequence[JsonDict],
    policy: Optional[LifecyclePolicy] = None,
    threshold: float = 0.5,
    corr_id: Optional[str] = None,
) -> Tuple[JsonDict, List[JsonDict]]:
    """
    Algorithm 1: Lifecycle Evidence Chaining in LIAC.

    This function generates a correlated lifecycle evidence chain across
    creation, distribution, installation, execution, and governance stages.
    """
    policy = policy or LifecyclePolicy()
    corr_id = corr_id or str(uuid4())

    chain: List[EvidenceRecord] = []
    prev_hash: Optional[str] = None

    artifact_hash = hash_json(artifact)
    creation = _make_record(
        stage="creation",
        corr_id=corr_id,
        payload={
            "artifact_hash": artifact_hash,
            "provenance": artifact.get("provenance", "unspecified"),
        },
        prev_hash=prev_hash,
        policy=policy,
    )
    chain.append(creation)
    prev_hash = creation.record_hash

    manifest_signature = hash_json({"manifest": manifest, "signed": True})
    distribution = _make_record(
        stage="distribution",
        corr_id=corr_id,
        payload={
            "artifact_hash": artifact_hash,
            "manifest_signature": manifest_signature,
            "release_metadata": manifest,
        },
        prev_hash=prev_hash,
        policy=policy,
    )
    chain.append(distribution)
    prev_hash = distribution.record_hash

    verification_succeeds = bool(target_device.get("verification_succeeds", True))
    installation_integrity = 1 if verification_succeeds else 0
    install_stage = "installation" if verification_succeeds else "installation-failure"
    installation = _make_record(
        stage=install_stage,
        corr_id=corr_id,
        payload={
            "deploy_id": target_device.get("deploy_id", "deploy-demo"),
            "device_id_hash": hash_json(target_device.get("device_id", "device-demo")),
            "attestation": target_device.get("attestation", "demo-attestation"),
            "installation_integrity": installation_integrity,
        },
        prev_hash=prev_hash,
        policy=policy,
    )
    chain.append(installation)
    prev_hash = installation.record_hash

    if not verification_succeeds:
        lir = {
            "corr_id": corr_id,
            "status": "installation-failure",
            "record_count": len(chain),
            "chain_head": prev_hash,
        }
        return lir, [record.to_dict() for record in chain]

    for event in execution_events:
        sdi, sdi_record = event_triggered_sdi_record_generation(
            installation_integrity=installation_integrity,
            behavior=event.get("behavior", {}),
            context=event.get("context", {}),
            threshold=threshold,
            corr_id=corr_id,
            timestamp=event.get("timestamp"),
        )
        if sdi == 1 and sdi_record is not None:
            execution = _make_record(
                stage="execution",
                corr_id=corr_id,
                payload=sdi_record,
                prev_hash=prev_hash,
                policy=policy,
                timestamp=sdi_record["timestamp"],
            )
            chain.append(execution)
            prev_hash = execution.record_hash

    governance = _make_record(
        stage="governance",
        corr_id=corr_id,
        payload={
            "policy": policy.storage_label,
            "accountability_action": "aggregate-and-preserve-lifecycle-record",
            "execution_records": sum(1 for record in chain if record.stage == "execution"),
        },
        prev_hash=prev_hash,
        policy=policy,
    )
    chain.append(governance)
    prev_hash = governance.record_hash

    lir = {
        "corr_id": corr_id,
        "status": "complete",
        "record_count": len(chain),
        "chain_head": prev_hash,
    }
    return lir, [record.to_dict() for record in chain]


def verify_chain(chain: Iterable[JsonDict]) -> bool:
    """
    Verify the basic hash linkage of a serialized evidence chain.

    This helper is provided for demonstration and tests.
    """
    previous_hash: Optional[str] = None
    for record in chain:
        if record.get("prev_hash") != previous_hash:
            return False

        unsigned = {
            "stage": record["stage"],
            "timestamp": record["timestamp"],
            "corr_id": record["corr_id"],
            "payload": record["payload"],
            "prev_hash": record["prev_hash"],
        }
        if hash_json(unsigned) != record.get("record_hash"):
            return False

        previous_hash = record.get("record_hash")
    return True
