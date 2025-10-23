from temporalio import workflow
from datetime import timedelta

@workflow.defn
class WorkflowC:
    @workflow.run
    async def run(self, input: str) -> str:
        from activities.activities import call_expensive_api
        
        result = await workflow.execute_activity(
            call_expensive_api,
            input,
            start_to_close_timeout=timedelta(seconds=30)
        )
        return f"\nWorkflow C completed: {result}"