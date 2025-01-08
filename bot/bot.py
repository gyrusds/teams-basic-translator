# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        print("Initializing MyBot...")
        load_dotenv()

        if "GOOGLE_API_KEY" not in os.environ:
            raise EnvironmentError(
                "Missing required environment variable: GOOGLE_API_KEY"
            )
        else:
            self.GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        prompt = ChatPromptTemplate.from_template(
            "system: You are a helpful assistant that translates to English.\nhuman: {input}"
        )
        self.chain = prompt | llm

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        translated_text = await self.translate_text(user_input)
        await turn_context.send_activity(translated_text)

    async def translate_text(self, text: str) -> str:
        try:
            translation = self.chain.invoke(
                {
                    "output_language": "English",
                    "input": text,
                }
            )
            return translation.content.strip()
        except Exception as e:
            print("Error llamando a LangChain/Azure OpenAI:", e)
            return "Lo siento, no pude traducir el texto."

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello! Welcome to TRANSLATOR chatbot. Please, introduce your question"
                )
