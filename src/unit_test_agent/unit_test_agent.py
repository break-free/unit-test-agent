from src.unit_test_agent.chains import CreateUnitTest, ReviewAndCorrectCode
from src.unit_test_agent.indexer import ConfirmVectorstoreCollectionIsEmpty, GetOrCreateVectorstore, SimilaritySearchVectorstore
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain.schema import BaseMemory
from langchain.schema.language_model import BaseLanguageModel
from src.unit_test_agent.tools import DummyTestCoverage, SaveToFile, RunTestSuiteTool, ReadFromLocalFile


class UnitTestAgent():

    llm: BaseLanguageModel
    conversational_memory: BaseMemory
    agent: AgentExecutor

    def __init__(self,
                 llm: BaseLanguageModel,
                 conversational_memory: BaseMemory):
        self.llm = llm
        self.conversational_memory = conversational_memory

        agent_tools = [DummyTestCoverage(),
                       ConfirmVectorstoreCollectionIsEmpty(),
                       GetOrCreateVectorstore(),
                       SimilaritySearchVectorstore(),
                       CreateUnitTest(llm),
                       SaveToFile(),
                       RunTestSuiteTool(),
                       ReviewAndCorrectCode(llm),
                       ReadFromLocalFile()]

        # initialize agent with tools
        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=agent_tools,
            llm=llm,
            verbose=True,
            memory=conversational_memory,
            return_intermediate_step=True
        )

    def run_agent(self, prompt: str):
        self.agent(prompt)
