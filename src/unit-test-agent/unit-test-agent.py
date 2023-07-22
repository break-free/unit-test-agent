from glob import glob
import indexer
import json
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
import os
import tools
from typing import Optional

# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
llm = ChatOpenAI(
    openai_api_key=os.environ['OPENAI_API_KEY'],
    temperature=0,
    model_name='gpt-3.5-turbo'
)

# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

tools = [tools.DummyTestCoverage(),
         indexer.ConfirmVectorstoreCollectionIsEmpty(),
         indexer.GetOrCreateVectorstore()]

# initialize agent with tools
agent = initialize_agent(
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)

agent("Determine what methods require additional testing. " +
      "Confirm if the local vectorstore is empty. " +
      "If the local vectorstore is empty create it using the directory `/var/home/chris/Projects/unit-test-agent/training/test`, otherwise use it as is.")
