from typing import Dict, Any, Optional
from llama_index.core import Settings
from llama_index.llms import LlamaCPP
from dataclasses import dataclass
from enum import Enum

MAX_REVIEWS = 3

class EventType(Enum):
    START = "start"
    CODE = "code"
    REVIEW = "review"
    PACKAGE = "package"
    MESSAGE = "message"
    STOP = "stop"

@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]

class Context:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._stream: list[Event] = []
    
    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)
    
    def write_event(self, event: Event) -> None:
        self._stream.append(event)

def truncate(text: str, max_length: int = 60) -> str:
    """Helper function to truncate long strings"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

class AppCreatorAgent:
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = "http://localhost:1234/v1"  # Default LM-Studio local server
        
        Settings.llm = LlamaCPP(
            model_url=model_path,
            temperature=0.7,
            context_window=4096,
            max_tokens=2048,
            generate_kwargs={"temperature": 0.7}
        )
        self.context = Context()

    async def architect(self, event: Event) -> Event:
        """Write initial code based on specification"""
        spec = event.data["input"]
        self.context.set("specification", spec)
        self.context.write_event(Event(
            type=EventType.MESSAGE,
            data={"msg": f"Writing app using this specification: {truncate(spec)}"}
        ))

        prompt = f"""Build an app for this specification: <spec>{spec}</spec>. 
        Make a plan for the directory structure you'll need, then return each file in full. 
        Don't supply any reasoning, just code."""
        
        code = await Settings.llm.complete(prompt)
        return Event(type=EventType.CODE, data={"code": code.text})

    async def coder(self, event: Event) -> Event:
        """Update code based on review"""
        spec = self.context.get("specification")
        review, code = event.data["review"], event.data["code"]
        
        self.context.write_event(Event(
            type=EventType.MESSAGE,
            data={"msg": f"Update code based on review: {truncate(review)}"}
        ))

        prompt = f"""We need to improve code that should implement this specification: <spec>{spec}</spec>. 
        Here is the current code: <code>{code}</code>. 
        And here is a review of the code: <review>{review}</review>. 
        Improve the code based on the review, keep the specification in mind, and return the full updated code. 
        Don't supply any reasoning, just code."""

        updated_code = await Settings.llm.complete(prompt)
        return Event(type=EventType.CODE, data={"code": updated_code.text})

    async def reviewer(self, event: Event) -> Event:
        """Review code and provide feedback"""
        spec = self.context.get("specification")
        code = event.data["code"]
        
        num_reviews = self.context.get("numberReviews", 0) + 1
        self.context.set("numberReviews", num_reviews)

        if num_reviews > MAX_REVIEWS:
            self.context.write_event(Event(
                type=EventType.MESSAGE,
                data={"msg": f"Already reviewed {num_reviews - 1} times, stopping!"}
            ))
            return Event(type=EventType.STOP, data={"result": code})

        self.context.write_event(Event(
            type=EventType.MESSAGE,
            data={"msg": f"Review #{num_reviews}: {truncate(code)}"}
        ))

        prompt = f"""Review this code: <code>{code}</code>. 
        Check if the code quality and whether it correctly implements this specification: <spec>{spec}</spec>. 
        If you're satisfied, just return 'Looks great', nothing else. 
        If not, return a review with a list of changes you'd like to see."""

        review = (await Settings.llm.complete(prompt)).text
        
        if "Looks great" in review:
            self.context.write_event(Event(
                type=EventType.MESSAGE,
                data={"msg": f"Reviewer says: {review}"}
            ))
            return Event(type=EventType.PACKAGE, data={"code": code})

        return Event(type=EventType.REVIEW, data={"review": review, "code": code})

    async def run(self, specification: str) -> str:
        """Run the full agent workflow"""
        event = Event(type=EventType.START, data={"input": specification})
        
        while True:
            if event.type == EventType.START:
                event = await self.architect(event)
            elif event.type == EventType.REVIEW:
                event = await self.coder(event)
            elif event.type == EventType.CODE:
                event = await self.reviewer(event)
            elif event.type == EventType.PACKAGE:
                return event.data["code"]
            elif event.type == EventType.STOP:
                return event.data["result"]

