from data_chunker import java_code as JCChunker
from data_chunker import parser as JCParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import BaseTool
from langchain.vectorstores import Chroma
from pydantic import BaseModel, BaseSettings, Field
from typing import Type

# Fields used in schemas
COLLECTION_NAME: str = Field(default="code_store",
                             description="the collection name in the vector store")
DIRECTORY: str = Field(default=".",
                       description="the directory where the code base is located")
TEXT: str = Field(default="",
                  description="text to search for in the vector store")


class VectorStoreSchema(BaseModel):

    # TODO: Replace these two with an actual vector store but still populate it by the agent. This
    #       way we can reuse the schema for an agent that updates the store.
    directory: str = DIRECTORY
    collection_name: str = COLLECTION_NAME


class VectorStoreSimilaritySearchSchema(BaseModel):

    # TODO: Replace the first variable with a vector store
    collection_name: str = COLLECTION_NAME
    text: str = TEXT


class ConfirmVectorStoreCollectionIsEmpty(BaseTool, BaseSettings):
    name = "Confirm Vector Store Collection Is Empty Tool"
    description = "use this tool to confirm if a vector store and its collection are empty"
    args_schema: Type[VectorStoreSchema] = VectorStoreSchema
    embedding_model: str = "text-embedding-ada-002"

    # TODO: Use a temporary file location, e.g., /tmp/db, to store the vector store as the
    #       default.
    persist_directory: str = "db"

    def _run(self, directory: str, collection_name: str):

        store = Chroma(collection_name=collection_name,
                       embedding_function=OpenAIEmbeddings(model=self.embedding_model),
                       persist_directory=self.persist_directory)
        if store._collection.count() == 0:
            return "Vector store is empty."
        else:
            return "Vector store contains items."

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class GetOrCreateVectorStore(BaseTool, BaseSettings):
    name = "Get or Create Vector Store Tool"
    description = (
        "use this tool to either create or get a vector store that contains a code base in the "
        "provided directory"
    )
    args_schema: Type[VectorStoreSchema] = VectorStoreSchema
    embedding_model: str = "text-embedding-ada-002"

    # TODO: Use a temporary file location, e.g., /tmp/db, to store the vector store as the
    #       default.
    persist_directory: str = "db"

    def _run(self, directory: str, collection_name: str):

        store = Chroma(collection_name=collection_name,
                       embedding_function=OpenAIEmbeddings(model=self.embedding_model),
                       persist_directory=self.persist_directory)

        if store._collection.count() != 0:
            return "Vector store already contains items therefore using as is."

        # TODO: The `+ "/src/main" is a hack to prevent this tool parsing all *.java files from
        #       both `main`, `test`, and `build` directories under `src` ; it needs to be updated
        #       with a better parameter, either here or in the calling agent.
        training_data = JCParser.get_file_list(directory + "/src/main", "*.java")

        chunks = []
        failed_files = []
        for file in training_data:
            codelines = JCParser.get_code_lines(file)
            try:
                tree = JCChunker.parse_code(file, codelines)
            except JCChunker.ParseError as e:
                failed_files.append(str(file) + ": " + str(e))
            if tree is not None:
                try:
                    # TODO: Replace with `chunk_all` function when available.
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

        store.add_texts(texts=str_chunks)

        return "Vector store created and populated with data."

    def _arun(self, directory: str):
        raise NotImplementedError("This tool does not support async")


class SimilaritySearchVectorStore(BaseTool, BaseSettings):
    name = "Similarity search in vector store"
    description = "use this tool to search a vector store collection for text"
    args_schema: Type[VectorStoreSimilaritySearchSchema] = VectorStoreSimilaritySearchSchema
    embedding_model: str = "text-embedding-ada-002"

    # TODO: Use a temporary file location, e.g., /tmp/db, to store the vector store as the
    #       default. Requires a bit more thought to make sure that the temp directory of either
    #       Linux or Windows is used.
    persist_directory: str = "db"

    def _run(self, collection_name: str, text: str):

        store = Chroma(collection_name=collection_name,
                       embedding_function=OpenAIEmbeddings(model=self.embedding_model),
                       persist_directory=self.persist_directory)

        return store.similarity_search(query=text, k=3)

    def _arun(self, collection_name: str, text: str):
        raise NotImplementedError("This tool does not support async")
