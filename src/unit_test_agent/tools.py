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


class SaveToFile(BaseTool):
    name = "Save To File Tool"
    description = (
        "use this tool to save code or text to disk using a specified file name"
    )
    args_schema: Type[SaveToFileSchema] = SaveToFileSchema

    def _run(self, file_path: str, content: str):
        print("File name: " + file_path)

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

        # TODO: This is a "hack" function added by necessity to remove additional lines and keep
        #       context minimal. Ideally, the test suite output would be changed to reflect needs,
        #       rather than doing it here!
        def filter_words_whitespace(text: str, filter_words: list[str]):
            # Split string by new line character.
            lines = text.split('\n')
            # Search for words in the provided list of words.
            filtered_lines = [line for line in lines if not any(word in line for word in filter_words)]
            # Remove any lines with only white space.
            nil_whitespace_lines = [line for line in filtered_lines if line.strip() != ""]
            # Return the joined string.
            return '\n'.join(nil_whitespace_lines)

        # TODO: The following command is fixed and uneditable; need to make it so the binary can be
        #       altered as needed
        process = subprocess.run(["./src/run_gradle.sh"],
                                 capture_output=True,
                                 text=True)
        if process.returncode != 0:
            filter_words = ['warning', 'WARNING', 'deprecated', 'BusinessDate', 'cucumber.core',
                            'RequestBody', 'getBean', 'found:', 'required:', 'where T is a',
                            'DEBUG']
            return "Errors were encountered\n\n" + filter_words_whitespace(process.stderr,
                                                                           filter_words)
        else:
            filter_words = ['WARNING', 'warning', 'deprecated', 'BusinessDate', 'cucumber.core',
                            'RequestBody', 'getBean', 'found:', 'required:', 'where T is a',
                            'DEBUG']
            return "No errors were encountered:\n\n" + filter_words_whitespace(process.stderr,
                                                                               filter_words)

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
