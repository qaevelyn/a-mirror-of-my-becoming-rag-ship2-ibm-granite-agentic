# Ship 2 — IBM Granite Agentic RAG Pipeline

**The moment the pipeline stopped being a lookup table.**

Ship 2 is the second pipeline in A Mirror of My Becoming, and the first with agency. Ship 1 answered questions from the corpus. Ship 2 decides what to do with the question — retrieve, act, or answer directly. It runs locally on IBM Granite. No cloud in the loop when it runs.

**Built:** August 2026 (originally on AWS SageMaker; moved local after Ship 1's loss)
**Author:** Evelyn Caro
**Status:** Built and working
**Part of A Mirror of My Becoming** — fleet index: [a-mirror-of-my-becoming-rag-pipelines](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-pipelines)

---

## What it does

An agentic RAG pipeline. Same retrieval architecture as Ship 1 — read documents, chunk them, embed them, store them — plus a decision layer at query time.

- Retrieve from the vector store when the answer lives in the corpus
- Call a tool or an API when the answer requires action
- Answer directly when the model already knows

The model chooses the path. That is what makes it agentic.

Nothing leaves the machine when the pipeline runs. No cloud account. No API key. No telemetry.

---

## What agentic looks like in practice

Standard RAG: always retrieve, then always generate. The pipeline is a lookup table with a language model on the end.

Agentic RAG: the model has access to retrieval and to tools, and it decides which to use. It can skip retrieval when the question is answerable from what it already knows. It can chain two steps when one is not enough. It can reach for a tool instead of answering from the corpus.

The pipeline does not force a path. The pipeline gives the model options, and the model picks.

**The full set of decisions is in the notebook's output cells.** Run the notebook to see the behavior: what it retrieved, what it called, what it answered directly.

---

## Requirements

The notebook names its own environment. Read the top of `Ship2_IBM_Granite_RAG_v2_Agentic.ipynb` before running. It lists the Python packages, the Ollama models, and the paths it expects.

**Setup:** [SETUP.md](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-pipelines/blob/main/SETUP.md) — three ways to point the pipeline at your own corpus.

---

## Quickstart

    # 1. Read the top of the notebook. Install what it names.
    # 2. Point the pipeline at a folder of documents (see SETUP.md).
    # 3. Run the notebook.
    #
    # The pipeline reads, chunks, embeds locally, and writes to a
    # local Chroma vector store. No cloud. No API key.

---

## Origin

Ship 2 exists because Ship 1 was not enough.

Ship 1 could retrieve and generate. It answered questions from the corpus. But it could not act. It could not reach beyond the chunks it had been given. It could not decide that a question needed a different path than retrieval.

Ship 2 added that layer. The model was given options — retrieve, act, answer — and it picked. The architecture started to feel less like a tool and more like a system.

What it made possible: questions Ship 1 could not answer, actions Ship 1 could not take, and a pipeline that worked like a small reasoning system instead of a lookup table.

Ship 2 was originally developed in an AWS SageMaker notebook environment. When Ship 1 was lost — the SageMaker instance terminated, the EBS volume corrupted, no AMI, no snapshot, no recovery path — the development posture of the fleet changed. Ship 2 was rebuilt and is now executed local-first. The cloud notebook layer is deprecated. **The pipeline runs on disk the author owns.**

---

## What Ship 2 does not do

- It does not upload anything. All processing is local.
- It does not call a cloud API when it runs. No OpenAI, no Anthropic, no Bedrock, no Vertex.
- It does not phone home. No telemetry. No analytics. No version check.
- It does not require an account. No sign-up. No API key. No credit card.

---

## Where the receipts live

The Ship 2 notebook is the primary source. Its output cells contain the pipeline's actual decisions during test runs — what it retrieved, what it called, what it answered directly. Run the notebook to see the behavior.

Ship 2 is also part of the group covered by **[Case Study: DeepSeek — The Benchmark](https://qaevelyn.github.io/white-papers/deepseek-case-study/)** — the paper written in August 2026 documenting the era in which Ships 1–4 were built.

A dedicated case study on Ship 2 — the shift from retrieval to agency — is in the pipeline.

---

## The fleet

Ship 2 of the A Mirror of My Becoming RAG pipelines fleet. The fleet index is [here](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-pipelines).

- **[Ship 1](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship1-deepseek)** — DeepSeek RAG, standard, rebuilt local after AWS lost it
- **Ship 2** — this repo — IBM Granite Agentic RAG
- **[Ship 3](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship3-ibm-granite)** — IBM Granite RAG, cross-platform
- **[Ship 4](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship4-ibm-granite-agentic)** — IBM Granite Agentic RAG, cross-platform
- **[Ship 5](https://github.com/qaevelyn/a-mirror-of-my-becoming-rag-ship5-ibm-granite-agentic-evidenceflow)** — IBM Granite Agentic RAG with EvidenceFlow

**[Suite: Ingestion Tools](https://github.com/qaevelyn/a-mirror-of-my-becoming-suite-ingestion-tools)** — the tooling that gets documents into the vector store this ship reads from.

**[A Mirror of My Becoming](https://github.com/qaevelyn/a-mirror-of-my-becoming)** — the parent index for the entire practice.

---

## License

Ship 2 is dual-licensed:

- **AGPL-3.0** — free to use, modify, and redistribute under the terms of the license. Full text in [LICENSE](LICENSE).
- **Commercial license** — available for organizations that need to use the code without the AGPL-3.0 obligations. Contact the author for pricing.

Free does not mean free to exploit. If you build a product on this work, the author expects to be paid.

---

## Author

**Evelyn Caro** — Sovereign AI Builder.

**[qaevelyn.github.io](https://qaevelyn.github.io)** · Commercial licensing: **evelyn.caro.cloud@gmail.com**

---

© 2026 Evelyn Caro. All rights reserved.
