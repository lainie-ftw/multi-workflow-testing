# Testing Strategies for Temporal Workflows that Call Other Workflows

This test suite provides comprehensive unit and integration testing for this set of workflows that call each other. Workflow A has an activity that calls Workflow B, which has an activity that calls Workflow C.

All workflows are started via `client.start_workflow` - alternatives include 1) using Signal with Start and 2) Child Workflows.

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── test_workflow_a.py       # Unit tests for WorkflowA
├── test_workflow_b.py       # Unit tests for WorkflowB
├── test_workflow_c.py       # Unit tests for WorkflowC
├── test_activities.py       # Unit tests for activities
```

## Test Categories

### 1. Unit Tests (Individual Workflows)

- **test_workflow_a.py**: Tests WorkflowA logic in isolation with mocked activities
- **test_workflow_b.py**: Tests WorkflowB logic in isolation with mocked activities
- **test_workflow_c.py**: Tests WorkflowC logic in isolation with mocked activities

### 2. Unit Tests (Activities)

- **test_activities.py**: Tests the call_expensive_api activity

### 3. Integration/End-to-End Testing

To accurately test the functionality of these workflows end to end, the `call_expensive_api` activity relies on an environmental variable that determines what logical environment the code is running it - if it's not running in production, call the `_mock_expensive_api_call` function, and if it is running in production, call the `_real_expensive_api_call` function. This allows the worker to be deployed to a real Temporal namespace, calling all real workflows and activities without incurring the cost of the API. 

## Key Testing Patterns

### Workflow Testing Pattern

Workflows are tested using Temporal's `WorkflowEnvironment` with time skipping:

```python
async def test_workflow(workflow_environment):
    # Create mock activity
    async def mock_activity(input: str) -> str:
        return "mocked result"
    
    # Set up worker with workflow and mock activity
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[MyWorkflow],
        activities=[mock_activity]
    ):
        # Execute workflow and verify result
        result = await workflow_environment.client.execute_workflow(...)
        assert "expected" in result
```

### Activity Testing Pattern

Activities are tested by mocking external dependencies:

```python
async def test_activity():
    # Mock the Temporal client
    mock_client = AsyncMock()
    mock_handle = AsyncMock()
    mock_handle.result = AsyncMock(return_value="result")
    mock_client.start_workflow = AsyncMock(return_value=mock_handle)
    
    # Patch dependencies and test
    with patch('shared.client.get_temporal_client', return_value=mock_client):
        result = await my_activity("input")
        assert result == "expected"
```
