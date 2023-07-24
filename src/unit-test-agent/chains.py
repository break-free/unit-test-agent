from langchain import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import Prompt
from langchain.tools import BaseTool, StructuredTool
import os
from pydantic import BaseModel, BaseSettings, Field
from typing import Type

# Fields used in StructuredTool schemas
CODE: str = Field( default = "", description = "the code that can be used to create a unit test")
LLM: BaseLanguageModel = Field( default = None, description = "the LLM to be used to assist with creating tests")

class CreateUnitTest(BaseTool):
    name = "Create Unit Test"
    description = (
        "use this tool to create a test class and unit tests for a code segment."
    )
    llm: BaseLanguageModel = None

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def _run(self, code:str):

        promptTemplate = """You are a world-class Java developer with an eagle eye for unintended bugs and edge cases. You carefully explain code with great detail and accuracy. You write careful, accurate unit tests. You only reply with code in a single block, without Markdown, and ready for saving to file. A good unit test should:
        - Test the function's behavior for a wide range of possible inputs
        - Test edge cases that the author may not have foreseen
        - Be easy to read and understand, with clean code and descriptive names
        - Be deterministic, so that the tests always pass or fail in the same way
        Use the following pieces of CodeContext to create a unit test.
        ---
        CodeContext: {context}
        """

        prompt = Prompt(template=promptTemplate, input_variables=["context"])
        llmChain = LLMChain(prompt=prompt, llm=self.llm)

        return str(llmChain.predict(prompt=prompt,
                                    context=code) )


    def _arun(self, code:str):
        raise NotImplementedError("This tool does not support async")
