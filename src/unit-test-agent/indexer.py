from data_chunker import java_code as JCChunker
from data_chunker import parser as JCParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import BaseTool, StructuredTool
from langchain.vectorstores import Chroma
from pydantic import BaseModel, BaseSettings, Field
from typing import Type

class VectorstoreSchema(BaseModel):
    directory: str = Field( default = ".", description = "where the code is located" )
    collection_name: str = Field( default = "code_store", description = "the name of the collection in the Chroma DB" )

class ConfirmVectorstoreCollectionIsEmpty(BaseTool, BaseSettings):
    name = "Confirm Vectorstore Collection Is Empty"
    description = (
        "use this tool to confirm is a vectorstore and its associated collection are empty"
    )
    args_schema: Type[VectorstoreSchema] = VectorstoreSchema
    embedding_model: str = "text-embedding-ada-002"
    persist_directory: str = "db"

    def _run(self, directory: str, collection_name: str):

        store = Chroma(collection_name=collection_name,
                       embedding_function=OpenAIEmbeddings(model=self.embedding_model),
                       persist_directory=self.persist_directory)
        if store._collection.count() == 0:
            return "Vectorstore is empty."
        else:
            return "Vectorstore contains items."

    def _arun(self, query:str):
        raise NotImplementedError("This tool does not support async")

class GetOrCreateVectorstore(BaseTool, BaseSettings):

    name = "Get or Create Vectorstore"
    description = (
        "use this tool to either create or get a Vectorstore from a provided folder containing a codebase"
        )
    args_schema: Type[VectorstoreSchema] = VectorstoreSchema
    embedding_model: str = "text-embedding-ada-002"
    persist_directory: str = "db"

    def _run(self, directory: str, collection_name: str):


        store = Chroma(collection_name=collection_name,
                       embedding_function=OpenAIEmbeddings(model=self.embedding_model),
                       persist_directory=self.persist_directory)

        if store._collection.count() != 0:
            return "Vectorstore already contains items therefore using as is."

        print(directory)
        training_data = JCParser.get_file_list(directory, "*.java")
        chunks = []
        failed_files = []
        for file in training_data:
            codelines = JCParser.get_code_lines(file)
            try:
                tree = JCChunker.parse_code(file, codelines)
            except JCChunker.ParseError as e:
                failed_files.append(str(file) + ": " + str(e))
            if tree != None:
                try:
                    chunks = chunks + JCChunker.chunk_constants(tree)
                    chunks = chunks + JCChunker.chunk_constructors(tree, codelines)
                    chunks = chunks + JCChunker.chunk_fields(tree, codelines)
                    chunks = chunks + JCChunker.chunk_methods(tree, codelines)
                except JCChunker.ChunkingError as e:
                    failed_files.append(str(file) + ": " + str(e))
            else:
                failed_files.append(str(file) + ", has no tree!")

        str_chunks = []
        for chunk in chunks:
            str_chunks.append(str(chunk))

        store.add_texts( texts=str_chunks )

        return "Vectorstore created and populated with data."

    def _arun(self, directory:str):
        raise NotImplementedError("This tool does not support async")
