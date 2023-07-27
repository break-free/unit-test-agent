import chains
import indexer
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
import os
import tools

# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
llm = ChatOpenAI(
    openai_api_key=os.environ['OPENAI_API_KEY'],
    temperature=0,
    model_name='gpt-4'
)

# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

tools = [tools.DummyTestCoverage(),
         indexer.ConfirmVectorstoreCollectionIsEmpty(),
         indexer.GetOrCreateVectorstore(),
         indexer.SimilaritySearchVectorstore(),
         chains.CreateUnitTest(llm),
         tools.SaveToNewFile(),
         tools.RunTestSuiteTool()]

# initialize agent with tools
agent = initialize_agent(
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    memory=conversational_memory,
    return_intermediate_step=True
)

# agent("Create one test class and as many unit tests as needed for each method reported by the test coverage tool in the same package as the method's class. Use the local vectorstore to retrieve information on the method, its class and its package as often as needed. If the vectorstore is empty, populate the vectorstore with code from the following directory '/var/home/chris/Projects/fineract/fineract-client'. Once created, the test class should be saved to disk using an appropriate file name and then tested. ")
agent("Run the test suite tool.")
