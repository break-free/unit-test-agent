from langchain.tools import BaseTool
from pydantic import BaseModel, BaseSettings, Field
from typing import Type

class DummyTestCoverage(BaseTool):
    name = "File Test Coverage Tool"
    description = (
        "use this tool to query for methods from classes within the codebase that require testing in JSON format"
    )

    def _run(self, query:str):
        return '{ class: "AccountType", method: "fromInt" }'

    def _arun(self, query:str):
        raise NotImplementedError("This tool does not support async")

class SaveToFileSchema(BaseModel):
    file_name: str = Field( default = "/tmp/ChangeFileName.txt", description = "file name including directory of where to save to disk")
    content: str = Field( default = "", description = "the content that will be saved to the file" )

class SaveToFile(BaseTool):
    name = "Save To File Tool"
    description = (
        "use this tool to save code or text to disk using a specified file name"
    )
    args_schema: Type[SaveToFileSchema] = SaveToFileSchema

    def _run(self, file_name: str, content: str):
        print("File name: " + file_name)
        print("Content: " + content)
        return "File '" + str(file_name) + "' saved, yay!"

    def _arun(self, file_name: str, content: str):
        raise NotImplementedError("This tool does not support async")
