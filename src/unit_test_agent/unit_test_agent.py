from src.unit_test_agent.chains import ReviewAndCorrectCode
from src.unit_test_agent.chains import CreateUnitTest
from src.unit_test_agent.indexer import ConfirmVectorStoreCollectionIsEmpty
from src.unit_test_agent.indexer import GetOrCreateVectorStore
from src.unit_test_agent.indexer import SimilaritySearchVectorStore
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import load_tools
from langchain.agents.agent import AgentExecutor
from langchain.schema import BaseMemory
from langchain.schema.language_model import BaseLanguageModel
from src.unit_test_agent.tools import DummyTestCoverage
from src.unit_test_agent.tools import DummyTestCoverageMultiple
from src.unit_test_agent.tools import SaveToLocalFile
from src.unit_test_agent.tools import RunTestSuiteTool
from src.unit_test_agent.tools import ReadFromLocalFile


class UnitTestAgent():

    llm: BaseLanguageModel
    conversational_memory: BaseMemory
    agent: AgentExecutor

    def __init__(self,
                 llm: BaseLanguageModel,
                 conversational_memory: BaseMemory):
        self.llm = llm
        self.conversational_memory = conversational_memory

        # TODO: This could also be passed into this class as a parameter, like `llm`, so maximum
        #       flexibility is achieved.
        agent_tools = load_tools(["human"], llm=llm)
        agent_tools.append(ConfirmVectorStoreCollectionIsEmpty())
        agent_tools.append(GetOrCreateVectorStore())
        agent_tools.append(SimilaritySearchVectorStore())
        agent_tools.append(SaveToLocalFile())
        agent_tools.append(ReadFromLocalFile())
        agent_tools.append(CreateUnitTest(llm))
        agent_tools.append(RunTestSuiteTool())
        agent_tools.append(ReviewAndCorrectCode(llm))

        # initialize agent with tools
        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=agent_tools,
            llm=llm,
            verbose=True,
            memory=conversational_memory,
            return_intermediate_step=True,
            max_iterations=100
        )

    def run_agent(self, prompt: str):
        self.agent(prompt)
