import asyncio
from agent import AppCreatorAgent
import os

async def main():
    # Initialize the agent with LM-Studio
    # You can override the default URL by providing your own
    agent = AppCreatorAgent(model_path="http://localhost:1234/v1")
    
    # Example specification
    specification = """
    Create a simple Flask web application that:
    1. Has a homepage with a welcome message
    2. Shows current time when you visit /time
    3. Has a basic CSS styling
    """
    
    # Run the agent
    result = await agent.run(specification)
    print("Final code generated:")
    print(result)
    
    # Package the code
    from packager import packager
    await packager(result)
    print("\nFiles have been created in the output directory")

if __name__ == "__main__":
    asyncio.run(main())

