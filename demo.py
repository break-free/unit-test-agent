#!/usr/bin/env python3

import argparse
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
import os
from src.unit_test_agent.unit_test_agent import UnitTestAgent
import sys

if __name__ == "__main__":

    # Check that environment variables are set up.
    if "OPENAI_API_KEY" not in os.environ:
        print("You must set an OPENAI_API_KEY using the Secrets tool", file=sys.stderr)

    # Create positional and optional command arguments
    parser = argparse.ArgumentParser(description="Create a vector store to pass contextual data to an LLM prompt")
    parser.add_argument('-c', '--show-context', action='store_true', dest='show_context', help='Show the context passed to the LLM.', default=False)
    parser.add_argument('data_path',
                        help='The location of the code base.',
                        default="fineract/fineract-client",
                        nargs='?')
    args = parser.parse_args()

    # initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
    llm = ChatOpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'],
        temperature=0,
        model_name='gpt-4'
    )

    # initialize conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=4,
        return_messages=True
    )

    prompt = f"Create one test class and as many unit tests as needed for each method reported by the test coverage tool in the same package as the method's class. Use the local vectorstore to retrieve information on the method, its class and its package as often as needed. If the vectorstore is empty, populate the vectorstore with code from the following directory '{args.data_path}'. Once created, the test class should be saved to disk using an appropriate file name and then tested, where you should identify errors and attempt to fix them. "

    agent = UnitTestAgent(llm, conversational_memory)

    agent.run_agent(prompt)
