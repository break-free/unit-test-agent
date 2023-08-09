from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import subprocess
from typing import Type

FILE_PATH = Field(default="",
                  description=(
                      "file path including directory of where to save to disk and the "
                      "file name, which should be in a standard location relative to "
                      "the original code"
                  )
                  )
CONTENT = Field(default="",
                description=(
                    "the content (e.g., code or text) that will be saved to a file"
                )
                )


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


class SaveToLocalFileSchema(BaseModel):

    file_path: str = FILE_PATH
    content: str = CONTENT


class SaveToLocalFile(BaseTool):

    name = "Save To File Tool"
    description = (
        "use this tool to save content (e.g., code or text) to disk using a specified file path"
    )
    args_schema: Type[SaveToLocalFileSchema] = SaveToLocalFileSchema

    def _run(self, file_path: str, content: str):
        with open(file_path, 'w') as f:
            f.write(content)
        return "File '" + str(file_path) + "' saved."

    def _arun(self, file_path: str, content: str):
        raise NotImplementedError("This tool does not support async")


class ReadFromLocalFile(BaseTool):

    name = "Read From Local File Tool"
    description = (
        "use this tool to read content (e.g., code or text) from a specified file path"
    )

    def _run(self, file_path: str):
        with open(file_path, 'r') as f:
            # TODO: Need to check that the file is not empty.
            return "File contents: " + f.read()

    def _arun(self, file_path: str):
        raise NotImplementedError("This tool does not support async")


class RunTestSuiteTool(BaseTool):

    name = "Run Test Suite Tool"
    description = (
        "use this tool to run the test suite and obtain results about failures, errors, and "
        "exceptions"
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
                                 text=True,
                                 shell=True)
        if process.returncode != 0:
            filter_words = ['cucumber.core', '0 Scenarios', '0 Steps', '0m0.', '--EclipseLink',
                            'BusinessDate', 'interfaceClass', '<T>getBean(Class<T>)', 'found: ',
                            'required: ', 'where T is a type-variable', 'RequestBody.create',
                            'warning', 'WARNING', 'DEBUG', '* ', '> ', '^']
            return "Errors were encountered:\n\n" + filter_words_whitespace(process.stderr + "\n" + process.stdout, filter_words)
        else:
            filter_words = ['0 Scenarios', '0 Steps', '0m0.', '--EclipseLink']
            return "Test results below:\n\n" + filter_words_whitespace(process.stdout,
                                                                       filter_words)

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
