import os
import anthropic
from dotenv import load_dotenv

load_dotenv("./AnthropicAPI/env")
class AnthropicAPI:
    def __init__(self) -> None:
        
        self.client = anthropic.Anthropic(
            # defaults to 
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    def create_message(self,message):
        message = self.client.messages.create(
            model="claude-2.1",
            max_tokens=1000,
            temperature=0,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return message.content[0].text
