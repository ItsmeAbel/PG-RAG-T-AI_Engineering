# PG-RAG-TC(Production Grade Retrieval-Augmented Generation with tool calling)
A production-style Retrieval-Augmented Generation (RAG) system with chunking, embedding, vector search, and evaluation, designed to minimize hallucinations and operate under real-world constraints. The data used for this project is a json sample data.

The web version of the tool can be found [ragincident:](https://ragincident.streamlit.app/)

# Tech stack
- Code: python
- Embedding: Gemeni
- Vector Store: FAISS
- LLM: Gemini
- Storage: Json, index, pickle
- Tool Calling: Gemeni. Langchain optional
- Evaluation: Python
- GUI: Streamlit
- Virtual Environment: venv

# Building process step-by-step
# Phase 1
1. Load Json data. Transfrom Data into one big text
2. Chunking: Break text into smaller chunks. Chunk size in this case is 80, which corresponds to about 80 words. Overlapp is set to about 10 words. 50 chunks in total.
3. Evaluation: chunking and overlapp is evaluated properly afterwards
4. Embedding: Embed the chunks using a gemeni embedding model. Batch embedding(batches of 10) is implemented for effectiveness. Each embedding got about 3072 dimensions.
5. Storing: Store embeddings in a vector store(vector databse) using FAISS
6. Query & Search: Turn user query into an embedding then do a semantic search that levarages ANN(Aproximate Nearest Neighbour) to find the closest(most similar) vectors in the database.
7. RAG: Implement a gemeni LLM model with predifined prompt that uses the vector database as context for its answer. The answer recieved is affected by the users choice of top-k and temperature. Top k= amount of nearest neigbours. Temperature = precison
8. GUI: Use streamlit(or any other method) to implement a simple GUI.

# phase 2: Make the system more Agentic by implementing tool calling
The goal here is to make the system automatically pick what actions to perform based on user query
- Gemini function calling is used for adding the tools
- currently, the system can choose between 2 action. Get live system metrics(mock) and/or show step-by-step solution to issues based on historical incidents
- more tools to be added...

# phase 3: Hallucination control
