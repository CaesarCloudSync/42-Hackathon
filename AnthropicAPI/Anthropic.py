import os
import anthropic
from dotenv import load_dotenv

load_dotenv("./AnthropicAPI/env")
class AnthropicAPI:
    def __init__(self) -> None:
        
        self.client = anthropic.Anthropic(
            # defaults to 
            api_key="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"

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
