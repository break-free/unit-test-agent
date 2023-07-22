from data_chunker import java_code as JCChunker
from data_chunker import parser as JCParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import BaseTool, StructuredTool
from langchain.vectorstores import Chroma
from pydantic import BaseModel, BaseSettings, Field
from typing import Type

class DummyTestCoverage(BaseTool):
    name = "File Test Coverage Tool"
    description = (
        "use this tool to obtain methods from classes within the codebase that require testing in JSON format."
    )

    def _run(self, query:str):
        return '{ class: "AccountType", method: "fromInt" }'

    def _arun(self, query:str):
        raise NotImplementedError("This tool does not support async")
