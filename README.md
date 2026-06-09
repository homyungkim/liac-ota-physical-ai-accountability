# LIAC Reference Implementation

Reference implementation for the algorithms described in the IEEE Access article:

**Structural Limits of Installation-Time Integrity Assurance: A Lifecycle-Based Accountability Framework for Over-the-Air-Enabled Physical AI Systems**

This repository provides a compact, reproducibility-oriented implementation of:

- **Algorithm 1:** Lifecycle Evidence Chaining in LIAC
- **Algorithm 2:** Event-Triggered SDI Record Generation

The implementation is intentionally lightweight. It is designed to clarify the evidence-generation and evidence-linkage logic of the Lifecycle Integrity and Accountability Coupling (LIAC) framework, not to serve as a production-grade secure logging, attestation, or runtime monitoring system.

## Repository scope

This code demonstrates how lifecycle evidence records can be generated and cryptographically linked across the following stages:

1. Creation
2. Distribution
3. Installation
4. Execution
5. Governance

It also demonstrates how a Semantic Deviation Indicator (SDI) evidence record may be emitted only when:

- installation-time artifact integrity remains valid,
- runtime behavior exits the semantic safety set, and
- the deviation measure exceeds a predefined triggering threshold.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── src/
│   └── liac/
│       ├── __init__.py
│       └── evidence.py
├── examples/
│   └── run_demo.py
└── tests/
    └── test_liac.py
```

## Quick start

Clone the repository and run the demonstration:

```bash
git clone https://github.com/<YOUR-GITHUB-ID>/liac-ota-physical-ai-accountability.git
cd liac-ota-physical-ai-accountability

python examples/run_demo.py
```

No external Python package is required for the core demonstration.

## Example output

The demo prints:

- a lifecycle correlation identifier,
- a linked lifecycle evidence chain,
- whether an SDI was emitted,
- the SDI evidence record when a semantically significant deviation occurs.

## Reproducibility note

The code is deterministic when a fixed correlation identifier is supplied. In the demo, record timestamps are generated at runtime; therefore, record hashes may differ across executions unless timestamps are fixed by the caller.

## Security note

This repository uses standard hash functions only for demonstration of evidence linkage. It does not implement production-grade secure storage, hardware-backed attestation, trusted execution, certificate validation, key management, or tamper-resistant logging. Such mechanisms should be supplied by the deployment environment.

## Suggested manuscript sentence

The following sentence may be added near Algorithm 1/2 or as a footnote in the final manuscript:

> To support reproducibility, a reference implementation of the LIAC evidence-chaining and event-triggered SDI record-generation procedures is publicly available at: https://github.com/<YOUR-GITHUB-ID>/liac-ota-physical-ai-accountability

Replace `<YOUR-GITHUB-ID>` with the actual GitHub account or organization name.

## License

This repository is released under the MIT License.
