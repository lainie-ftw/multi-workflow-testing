from temporalio import workflow
from datetime import timedelta

@workflow.defn
class WorkflowA:
    @workflow.run
    async def run(self, input: str) -> str:
        # Import activities here
        from activities.activities import activity_start_workflow_b

        # Activity starts Workflow B
        result = await workflow.execute_activity(
            activity_start_workflow_b,
            input,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        return f"Workflow A completed: {result}"