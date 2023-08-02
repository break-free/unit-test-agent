from langchain import LLMChain
from langchain.base_language import BaseLanguageModel
from langchain.prompts import Prompt
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# Fields used in schemas
CLASS_NAME: str = Field(default="",
                        description="the name of the class containing the method to be tested")
CODE: str = Field(default="",
                  description="the code that requires a new or amended unit test")
ERRORS: str = Field(default="",
                    description=(
                        "the errors by a test suite that were generated due to coding errors"
                    )
                    )
FAILED_CODE: str = Field(default="",
                         description="the code that failed testing and requires amendment")
PACKAGE_NAME: str = Field(default="",
                          description="the package that the test class must belong to")


class CreateUnitTestSchema(BaseModel):
    package_name: str = PACKAGE_NAME
    class_name: str = CLASS_NAME
    code: str = CODE


class CreateUnitTest(BaseTool):
    name = "Create Unit Test"
    description = (
        "use this tool to create a test class and unit tests for a code segment."
    )
    args_schema: Type[CreateUnitTestSchema] = CreateUnitTestSchema
    llm: BaseLanguageModel = None

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def _run(self, package_name: str, class_name: str, code: str):

        promptTemplate = """You are a world-class Java developer with an eagle eye for unintended bugs and edge cases. You carefully explain code with great detail and accuracy. You write careful, accurate unit tests. You only reply with well-commented code in a single block, without Markdown, and ready for saving to file. A good unit test should:
        - Test the function's behavior for a wide range of possible inputs
        - Test edge cases that the author may not have foreseen
        - Be easy to read and understand, with clean code and descriptive names
        - Be deterministic, so that the tests always pass or fail in the same way
        Use the following pieces of CodeContext to create a unit test.
        ---
        PackageName: {package_name}
        ---
        ClassName: {class_name}
        ---
        CodeContext: {context}
        """

        prompt = Prompt(template=promptTemplate,
                        input_variables=["package_name", "class_name", "context"])
        llmChain = LLMChain(prompt=prompt, llm=self.llm)

        return str(llmChain.predict(prompt=prompt,
                                    package_name=package_name,
                                    class_name=class_name,
                                    context=code))

    def _arun(self, code: str):
        raise NotImplementedError("This tool does not support async")


class ReviewAndCorrectCodeSchema(BaseModel):
    code: str = FAILED_CODE
    errors: str = ERRORS


class ReviewAndCorrectCode(BaseTool):
    name = "Review and correct code tool"
    description = (
        "use this tool to submit code and associated error for review and correction"
    )
    args_schema: Type[ReviewAndCorrectCodeSchema] = ReviewAndCorrectCodeSchema
    llm: BaseLanguageModel = None

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def _run(self, code: str, errors: str):

        promptTemplate = """You are a world-class Java developer with an eagle eye for unintended bugs. You review and correct unit tests. You only reply with well-commented code in a single block, without Markdown, and ready for saving to file. A corrected unit test should:
        - Resolve any identifiable errors
        - Focus on removing rather than adding code but add only when necessary
        - Be easy to read and understand, with clean code and descriptive names
        Use the following pieces of CodeContext and Errors to review and correct the unit test.
        ---
        CodeContext: {code}
        ---
        Errors: {errors}
        """

        prompt = Prompt(template=promptTemplate,
                        input_variables=["code", "errors"])
        llmChain = LLMChain(prompt=prompt, llm=self.llm)

        return str(llmChain.predict(prompt=prompt,
                                    code=code,
                                    errors=errors))

    def _arun(self, code: str, errors: str):
        raise NotImplementedError("This tool does not support async")
