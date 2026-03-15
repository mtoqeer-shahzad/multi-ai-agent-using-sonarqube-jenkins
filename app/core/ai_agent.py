from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings


def get_ai_agent_response(model_id, query, allow_search, system_prompt):

    # Step 1: Groq LLM load karo
    llm = ChatGroq(
        model=model_id,
        api_key=settings.GROQ_API_KEY
    )

    # Step 2: Tavily tool — allow_search True ho toh ON, warna empty list
    tools = [TavilySearchResults(
        max_results=2,
        tavily_api_key=settings.TAVILY_API_KEY
    )] if allow_search else []

    # Step 3: ReAct Agent banao
    # ✅ FIX: LangGraph new version mein state_modifier → prompt ho gaya
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt       # ✅ state_modifier nahi — prompt likhna hai
    )

    # Step 4: User query state mein pack karo
    state = {
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    # Step 5: Agent invoke karo
    response = agent.invoke(state)

    # Step 6: Messages list nikalo
    messages = response.get("messages")

    # Step 7: Sirf AIMessage filter karo
    ai_messages = [
        message.content for message in messages
        if isinstance(message, AIMessage)
    ]

    # Step 8: Last AI message return karo (final answer)
    return ai_messages[-1]