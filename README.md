# Order Assistant (LangChain + Python)

A conversational AI assistant that answers natural-language questions about orders,
customers, and products by calling a live REST API as tools — built on top of the
companion [Order Management System](../order-management-system) project.

Ask things like:
- "What's the status of order 5?"
- "Show me all orders for customer 2"
- "Do you have any products matching 'headphones'?"

The assistant uses a tool-calling LLM agent: instead of guessing answers, it decides
which tool to call, hits the real Django API, and answers using the actual data returned.

## Why this project

Most LangChain demos hard-code fake data or a static document. This one is wired to a
real backend service, which mirrors how AI features actually get integrated into
existing products — the LLM is a layer on top of real APIs, not a replacement for them.

## Tech Stack

- Python 3.11+
- LangChain (tool-calling agents)
- Google Gemini, Anthropic Claude, or OpenAI GPT (your choice, via `.env`)
- Requests (to call the Django REST API)

## Architecture

```
User → CLI (main.py) → Agent (agent.py) → Tools (tools.py) → Django REST API
                              ↓
                        LLM decides which
                        tool(s) to call
```

## Prerequisites

This project **calls** the Order Management System API, so that project must be running
first. Clone and run it separately: see its own README for setup, then start it with:
```bash
python manage.py runserver
```

You'll also need an API key for Gemini (recommended — has a free tier), Anthropic, or
OpenAI. Get a free Gemini key at https://aistudio.google.com/apikey.

## Setup & Run

```bash
# 1. Clone this repo
git clone https://github.com/<your-username>/order-assistant.git
cd order-assistant

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then edit .env and add your API key + confirm DJANGO_API_BASE_URL

# 5. Make sure the Django Order Management System is running (in a separate terminal)

# 6. Run the assistant
python main.py
```

## Example session

```
You: What's the status of order 3?
Assistant: Order #3 is currently 'Shipped'. Total: 59.98. Items: 2x Wireless Mouse.

You: Do you have anything matching 'keyboard'?
Assistant: Mechanical Keyboard - $79.99 (12 in stock)
```

## Project Structure

```
order-assistant/
├── main.py           # CLI chat loop
├── agent.py           # LangChain agent + LLM setup
├── tools.py            # Tools that call the Django API
├── config.py           # Environment-based configuration
├── .env.example
└── requirements.txt
```

## Roadmap / Possible Extensions

- Add a tool to create orders, not just read them
- Swap the CLI for a small FastAPI/Streamlit chat UI
- Add conversation memory persistence across sessions
- Add streaming responses
- Write tests using LangChain's fake/mock LLM for deterministic tool-call testing

## License

MIT
