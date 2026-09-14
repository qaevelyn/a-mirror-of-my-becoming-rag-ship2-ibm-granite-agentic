# Ship 2: IBM Granite Agentic RAG Pipeline

**Built:** August 2026
**Author:** Evelyn Caro
**Status:** ✅ Built and working

**Naming note:** The folder is named `ship2-aws-agentic-rag`. The code files are named 
`Ship2_IBM_Granite_RAG_v2_Agentic`. Both are accurate: the pipeline was originally 
developed in an AWS SageMaker notebook environment, and the model used is IBM Granite. 
The folder name reflects the platform; the file names reflect the model. Current 
execution is local-first, no cloud dependency.

---

## Origin

The second ship added agency.

Ship 1 could retrieve and generate. Ship 2 could decide. The pipeline learned to choose 
when to reach for data, when to act on it, when to call an API and when to answer directly. 
This is where the architecture started to feel like a system — not a tool.

---

## What It Does

An agentic RAG pipeline built on IBM Granite. Retrieval + action. The agent decides when 
to query the vector database, when to call APIs, and when to answer from what it already 
knows.

---

## Architecture

- **Runtime:** Local, sovereign execution
- **Model:** IBM Granite
- **Pipeline:** Agentic RAG
- **Data source:** Local files — the Mirror personal archive
- **Storage:** Vector database (ChromaDB)
- **Cloud dependency:** None (current)

---

## Pipeline

1. Read local documents from the Mirror archive
2. Chunk into pieces
3. Vectorize (embed) each chunk
4. Store vectors in a vector database
5. Query at runtime → the agent decides whether to retrieve, call an API, or answer directly

---

## Integration

- Reads local data — the Mirror personal archive
- Chunks, vectorizes, stores in vector DB
- Agent decides when to query, when to act, when to answer
- **No cloud dependency.** Local-first. Sovereign.
- Early builds ran in an AWS SageMaker notebook environment. The cloud notebook layer 
  is deprecated; execution is now local-first.

---

## Access and Copyright

This work was created by Evelyn Caro. DeepSeek is the only collaborator — used as a tool 
in the creative and technical process.

This is a personal portfolio project and is not open for collaboration or external access. 
The video and documentation speak for themselves.

Copyright © 2026 Evelyn Caro. All rights reserved. Copyright registration is pending.
