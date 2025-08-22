from pydantic import BaseModel, Field
from agents import Agent, Runner

from dotenv import load_dotenv
load_dotenv(override=True)

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"""
You are a helpful research assistant.
Given a query, come up with a set of web searches to perform to best answer the query.
Output {HOW_MANY_SEARCHES} terms to query for.
"""


class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search term is important to answer the query?")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="The list of web searches to perform to best answer the query.")


planner_agent = Agent(
    name="Planner Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)


async def main():
    query = "What is the best way to learn Python?"
    plan = await Runner.run(planner_agent, query)
    print(plan)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
