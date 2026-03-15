# 🤖 AI-Powered Virtual Development Pod

A multi-agent AI framework that simulates a real IT development team. Given a high-level business requirement, the system automatically produces **user stories**, **system design**, **source code**, and **test cases**.

## Architecture

```
User (Requirement)
       │
  Streamlit Dashboard / CLI
       │
  Project Lead Agent
       │
  ┌────┼────┬────┐
  ▼    ▼    ▼    ▼
 BA  Design Dev  Test
```

**Pipeline**: Business Analyst → Design Agent → Developer Agent → Testing Agent

All artifacts are saved as markdown and embedded into **ChromaDB** vector memory.

## Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
# Create .env file with:
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
TEMPERATURE=0.2
```

Get a free API key from [Groq Console](https://console.groq.com/).

## Running

### Streamlit Dashboard

```bash
streamlit run frontend/streamlit_app.py
```

### CLI Mode

```bash
python main.py
```

## Project Structure

```
agents/          # CrewAI agent definitions
tasks/           # CrewAI task definitions
memory/          # ChromaDB vector store
artifacts/       # Artifact file manager
frontend/        # Streamlit dashboard
config/          # Prompt templates (YAML)
templates/       # Markdown templates
main.py          # CLI entry point
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Orchestration | CrewAI |
| LLM | Groq (Llama 3.1) via LangChain |
| Vector Memory | ChromaDB |
| Frontend | Streamlit |
