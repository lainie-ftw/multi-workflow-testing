# Testing Strategies for Temporal Workflows that Call Other Workflows

This test suite provides comprehensive unit and integration testing for this set of workflows that call each other. Workflow A has an activity that calls Workflow B, which has an activity that calls Workflow C.

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── test_workflow_a.py       # Unit tests for WorkflowA
├── test_workflow_b.py       # Unit tests for WorkflowB
├── test_workflow_c.py       # Unit tests for WorkflowC
├── test_activities.py       # Unit tests for activities
└── README.md               # This file
```

## Test Categories

### 1. Unit Tests (Individual Workflows)

- **test_workflow_a.py**: Tests WorkflowA logic in isolation with mocked activities
- **test_workflow_b.py**: Tests WorkflowB logic in isolation with mocked activities
- **test_workflow_c.py**: Tests WorkflowC logic in isolation with mocked activities

### 2. Unit Tests (Activities)

- **test_activities.py**: Tests the call_expensive_api activity

### 3. Integration/End-to-End Testing

To accurately test the functionality of these workflows end to end, the `call_expensive_api` activity relies on an environmental variable that determines what logical environment the code is running it - if it's not running in production, call the `_mock_expensive_api_call` function, and call the `_real_expensive_api_call` function if it is running in production. This allows the worker to be deployed to a real Temporal environment and call all real workflows and activities without hitting the API. 

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run specific test file:
```bash
pytest tests/test_workflow_a.py
pytest tests/test_activities.py
```

### Run with verbose output:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ --cov=workflows --cov=activities --cov-report=html
```

### Run specific test:
```bash
pytest tests/test_workflow_a.py::test_workflow_a_successful_execution
```

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
