#!/usr/bin/env python3
# ============================================================
# Copyright (c) 2026 Evelyn Caro. All rights reserved.
# A Mirror of My Becoming
# https://evelynacaro.github.io
# For licensing inquiries: evelyn.caro.cloud@gmail.com
# ============================================================

"""
Ship 2 — IBM Granite Agentic RAG — Demo Script
Uses the existing chroma_db vector store. No document loading.
"""
import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
print("Ship 2 — IBM Granite Agentic RAG")
print("─" * 50)

# Load existing vector store
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
print(f"✅ Vector store loaded: {vector_store._collection.count()} documents")

# Load the LLM
llm = ChatOllama(model="granite4.1:3b", temperature=0.7)
print("✅ LLM ready: granite4.1:3b")
print()

# ------------------------------------------------------------
# Agentic tool — the LLM decides when to call this
# ------------------------------------------------------------
@tool
def get_granite_context(question: str) -> str:
    """Retrieve relevant context from the Mirror archive."""
    results = retriever.invoke(question)
    return "\n\n".join(doc.page_content for doc in results)

tools = [get_granite_context]
llm_with_tools = llm.bind_tools(tools)

# ------------------------------------------------------------
# Run one query — agentic flow
# ------------------------------------------------------------
queries = [
    "What is the Mirror of My Becoming?",
    "When did Evelyn start building the Mirror project?",
    "What ships has Evelyn built?",
]
for query in queries:
    print(f"Query: {query}")
    print("─" * 50)
    response = llm_with_tools.invoke(query)
    if response.tool_calls:
        print(f"🔧 Agent decided to call: {response.tool_calls[0]['name']}")
        tool_result = get_granite_context.invoke(response.tool_calls[0]['args'])
        final = llm.invoke(f"Context:\n{tool_result}\n\nQuestion: {query}\n\nAnswer:")
        print()
        print("Answer:")
        print(final.content)
    else:
        print("Agent answered directly:")
        print(response.content)
    print()

print()
print("─" * 50)
print("Demo complete.")
