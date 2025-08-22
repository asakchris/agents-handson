from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio

class ResearchManager:
    async def run(self, query: str):
        """Run the deep research process, yielding the status updates and the final report."""
        trace_id = gen_trace_id()
        with trace("ResearchManager", trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            print("Starting research process...")
            search_plan = await self.plan_searches(query)
            yield f"Planned {len(search_plan.searches)} searches, starting now..."
            
            search_results = await self.perform_searches(search_plan)
            yield f"Completed {len(search_results)} searches, writing report..."
            
            report = await self.write_report(query, search_results)
            yield f"Completed report, sending email..."
            
            await self.send_email(report)
            yield f"Email sent, research complete."

            yield report.markdown_report
            
    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the web searches to perform to best answer the query."""
        print("Planning web searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        print(f"Will perform {len(result.final_output.searches)} searches.")
        return result.final_output_as(WebSearchPlan)
        
    async def perform_searches(self, plan: WebSearchPlan) -> list[str]:
        """Perform the web searches."""
        print("Performing web searches...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(search_item)) for search_item in plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Completed {num_completed} of {len(tasks)} searches.")
        print("Finished performing web searches.")
        return results
        
    async def search(self, search_item: WebSearchItem) -> str:
        """Perform a single web search."""
        input = f"Search term: {search_item.query}\nReason for searching: {search_item.reason}"
        try:
            result = await Runner.run(search_agent, input)
            return str(result.final_output)
        except Exception as e:
            print(f"Error performing search: {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write a report based on the web searches."""
        print("Writing report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input)
        print("Finished writing report.")
        return result.final_output_as(ReportData)
        
    async def send_email(self, report: ReportData) -> None:
        """Send the report via email."""
        print("Sending email...")
        await Runner.run(email_agent, report.markdown_report)
        print("Finished sending email.")
        return report
