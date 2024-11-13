import pytest
import asyncio
from agent import AppCreatorAgent, Event, EventType
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_architect():
    agent = AppCreatorAgent(model_path="http://localhost:1234/v1")
    event = Event(type=EventType.START, data={"input": "Create a hello world Flask app"})
    
    with patch('llama_index.core.Settings.llm.complete', new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value.text = "app.py\n```python\nfrom flask import Flask\n```"
        result = await agent.architect(event)
        
        assert result.type == EventType.CODE
        assert "flask" in result.data["code"].lower()

@pytest.mark.asyncio
async def test_reviewer():
    agent = AppCreatorAgent(model_path="http://localhost:1234/v1")
    agent.context.set("specification", "Create a hello world Flask app")
    event = Event(type=EventType.CODE, data={"code": "from flask import Flask"})
    
    with patch('llama_index.core.Settings.llm.complete', new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value.text = "Looks great"
        result = await agent.reviewer(event)
        
        assert result.type == EventType.PACKAGE
        assert "flask" in result.data["code"].lower()

if __name__ == "__main__":
    asyncio.run(pytest.main([__file__]))
