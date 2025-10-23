from temporalio import workflow
from datetime import timedelta

@workflow.defn
class WorkflowB:
    @workflow.run
    async def run(self, input: str) -> str:
        # Import activities here
        from activities.activities import activity_start_workflow_c

        # Activity starts Workflow C
        result = await workflow.execute_activity(
            activity_start_workflow_c,
            input,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        return f"\nWorkflow B completed: {result}"