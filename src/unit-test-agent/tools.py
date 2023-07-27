from langchain.tools import BaseTool
import os
from pydantic import BaseModel, Field
import subprocess
from typing import Type


class DummyTestCoverage(BaseTool):
    name = "File Test Coverage Tool"
    description = (
        "use this tool to query for methods from classes within the codebase that require testing "
        "in JSON format"
    )

    def _run(self, query: str):
        return '{ class: "Parts", method: "fromFile" }'

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class SaveToFileSchema(BaseModel):
    file_path: str = Field(default="/tmp/ChangeFileName.txt",
                           description=(
                               "file path including directory of where to save to disk and the "
                               "file name"
                           )
                           )
    content: str = Field(default="", description="the content that will be saved to the file")


class SaveToNewFile(BaseTool):
    name = "Save To New File Tool"
    description = (
        "use this tool to save code or text to disk using a specified file name"
    )
    args_schema: Type[SaveToFileSchema] = SaveToFileSchema

    def _run(self, file_path: str, content: str):
        print("File name: " + file_path)
        print("Content: " + content)

        if os.path.isfile(file_path):
            if os.path.getsize(file_path) > 0:
                return "File '" + str(file_path) + "' exists and contains content!"
        with open(file_path, 'w') as f:
            f.write(content)
        return "File '" + str(file_path) + "' saved."

    def _arun(self, file_path: str, content: str):
        raise NotImplementedError("This tool does not support async")


class RunTestSuiteTool(BaseTool):
    name = "Run Test Suite Tool"
    description = (
        "use this tool to run the test suite and obtain results about failures, errors, and exceptions"
    )

    def _run(self):
        # TODO: The following command is fixed and uneditable; need to make it something we can pass to the tool
        process = subprocess.run(["/var/home/chris/Projects/unit-test-agent/src/run_gradle.sh"],
                                 capture_output=True,
                                 text=True)
        if process.returncode != 0:
            return "Errors were encountered\n\n" + process.stderr
        else:
            return "The output from the test suite is below:" + process.stdout

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
