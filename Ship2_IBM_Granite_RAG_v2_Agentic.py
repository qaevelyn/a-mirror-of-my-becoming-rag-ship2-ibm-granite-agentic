#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Ship 2: IBM Granite Mirror RAG Pipeline

# Adapted for: A Mirror of My Becoming - Sovereign personal archive
# Author: Evelyn Caro (@qaevelyn)


# In[ ]:


## About This Notebook

This notebook builds a Retrieval-Augmented Generation (RAG) pipeline for A Mirror of My Becoming - a sovereign personal archive.

What this notebook does:
1. Loads Mirror documents (PDFs, Markdown, text files)
2. Splits them into chunks
3. Creates embeddings using IBM Granite (via Ollama)
4. Stores them in a vector database (ChromaDB)
5. Queries the archive and generates responses

Based on: IBM SkillsBuild Lab - Build a RAG Pattern with LangChain
Adapted by: Evelyn Caro (@qaevelyn)
Mission: Sovereign data ownership for Foundational Black Americans and Freedmen


# In[ ]:


## 1. Set Up Environment


# In[ ]:


### 1a. Install Dependencies


# In[18]:


from langchain_ollama import OllamaEmbeddings

# Use nomic-embed-text for embeddings (supports Ollama embeddings)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Tokenizer placeholder (not needed for Ollama)
embeddings_tokenizer = None

print("✅ Embeddings ready with nomic-embed-text")

from langchain_ollama import OllamaEmbeddings

# Use nomic-embed-text for embeddings (supports Ollama embeddings)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Tokenizer placeholder (not needed for Ollama)
embeddings_tokenizer = None

print("✅ Embeddings ready with nomic-embed-text")

from langchain_chroma import Chroma

# We'll create the vector store after we have the documents
# For now, just import the library
print("✅ ChromaDB imported")

from langchain_ollama import ChatOllama, OllamaEmbeddings

# Use IBM Granite via Ollama (no stop parameter)
llm = ChatOllama(
    model="granite4.1:3b",
    temperature=0.7,
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

print("✅ Model and embeddings ready")
print("✅ LLM ready with granite4.1:3b")

from langchain_chroma import Chroma

# Create vector store from the text chunks
vector_store = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Vector store created with", len(texts), "chunks")

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# Run a similarity search
query = "Why are you interested in this program?"
results = retriever.invoke(query)

print(f"Found {len(results)} relevant chunks")
for i, doc in enumerate(results):
    print(f"\n--- Chunk {i+1} ---")
    print(doc.page_content[:200] + "...")


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

# Use PyPDFLoader for PDF files
loader = PyPDFLoader(file_path)
documents = loader.load()

text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separator="\n",
)

texts = text_splitter.split_documents(documents)

doc_id = 0
for text in texts:
    text.metadata["doc_id"] = (doc_id:=doc_id+1)

print(f"{len(texts)} text document chunks created")


# In[4]:


## 3. Load and Chunk Document


# In[21]:


import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# Define the file path
file_path = "/Users/evelyn/Documents/Mirror-Project/MIRROR_LOG.md"

if os.path.exists(file_path):
    print(f"✅ Loading: {file_path}")
    loader = TextLoader(file_path)
    documents = loader.load()
else:
    print(f"❌ File not found: {file_path}")
    # Fallback to state_of_the_union
    import wget
    url = "https://raw.githubusercontent.com/IBM/watson-machine-learning-samples/master/cloud/data/foundation_models/state_of_the_union.txt"
    filename = "state_of_the_union.txt"
    if not os.path.exists(filename):
        wget.download(url, out=filename)
    loader = TextLoader(filename)
    documents = loader.load()

# Split into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separator="\n",
)

texts = text_splitter.split_documents(documents)

print(f"✅ Created {len(texts)} chunks")


# In[ ]:


## 4. Create Vector Store


# In[22]:


from langchain_chroma import Chroma

# Create vector store from the text chunks
vector_store = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Vector store created")


# In[ ]:


## 5. Query the RAG Pipeline


# In[23]:


# Generate a retrieval-augmented response
query = "Why are you interested in this program?"
results = retriever.invoke(query)

# Combine context
context = "\n\n".join([doc.page_content for doc in results])

# Generate response
response = llm.invoke(f"Based on the following context, answer the question: {query}\n\nContext: {context}")
print(response.content)
print(f"Question: {query}\n")
print("Answer:")
print(response.content)


# In[ ]:


## 6. Define the RAG Tool


# In[25]:


from langchain_classic.tools import tool

# Create retriever (if not already defined)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

@tool
def get_granite_context(question: str) -> str:
    """Retrieve relevant context from the Mirror archive."""
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

tools = [get_granite_context]


# In[ ]:


## 7. Set Up the Agent Prompt


# In[26]:


from langchain_classic.tools.render import render_text_description_and_args
from langchain_core.prompts import ChatPromptTemplate

system_prompt = """You are a helpful AI assistant. You have access to a tool that can retrieve relevant context from a personal archive.

Use the tool to answer questions when you don't have the information.

Provide only ONE action per JSON blob.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)


# In[ ]:


## 8. Set Up Agent Memory and Chain


# In[27]:


from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

template = """You are a helpful assistant. You have access to the following tools:

{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,  # Limit to 3 loops to prevent infinite
)


# In[ ]:


## 9. Run the Agentic RAG Query


# In[ ]:


response = agent_executor.invoke({
    "input": "What is the main topic of the document?"
})

print("="*60)
print("QUESTION: What is the main topic of the document?")
print("="*60)
print(response["output"])

