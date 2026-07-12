from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import LLM_PROVIDER, GOOGLE_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY
from tools import ALL_TOOLS

SYSTEM_PROMPT = """You are a helpful customer support assistant for an online store.
You can look up order status, list a customer's orders, and search the product catalog
using the tools available to you. Always use a tool to fetch real data rather than
guessing or making up order or product details. If a tool returns an error or says
nothing was found, tell the user clearly instead of inventing an answer.
Keep responses concise and friendly."""


def build_llm():
    """Instantiate the chat model based on LLM_PROVIDER in config.py / .env."""
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        if not OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your .env file."
            )
        return ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file."
            )
        return ChatAnthropic(
            model="claude-3-5-sonnet-latest", temperature=0, api_key=ANTHROPIC_API_KEY
        )

    # Default: Gemini (has a free tier, good for personal projects)
    from langchain_google_genai import ChatGoogleGenerativeAI

    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to your .env file."
        )
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", temperature=0, google_api_key=GOOGLE_API_KEY
    )


def build_agent_executor() -> AgentExecutor:
    llm = build_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, ALL_TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=ALL_TOOLS, verbose=True)
