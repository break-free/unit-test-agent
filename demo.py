#!/usr/bin/env python3

import argparse
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
import os
from src.unit_test_agent.unit_test_agent import UnitTestAgent
import sys

if __name__ == "__main__":

    # Check that environment variables are set up.
    if "OPENAI_API_KEY" not in os.environ:
        print("You must set an OPENAI_API_KEY using the Secrets tool", file=sys.stderr)

    # Create positional and optional command arguments
    parser = argparse.ArgumentParser(
        description="Create a vector store to pass contextual data to an LLM prompt"
    )
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

    # initialize conversational memory using tokens
    conversational_memory = ConversationTokenBufferMemory(
        llm=llm,
        max_token_limit=5000,
        return_messages=True,
        verbose=True
    )

    agent = UnitTestAgent(llm, conversational_memory)

    # Create a unit test and then attempt to fix the errors #
    prompt = f"Create test classes for each class and method reported by the test coverage tool until no more are provided. Use the local vector store to retrieve information on the method, its class and its package. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created the test class should be saved to disk using an appropriate file name within `{args.data_path}`, and then tested. If there are any errors then attempt to fix them until resolved."

    # A human in the loop prompt ##
    # prompt = f"Create one test class as needed for each method reported by the test coverage tool. Use the local vector store to retrieve information on the method, its class and its package as often as needed. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created, the test class should be saved to disk using an appropriate file name, checked by a human, and then tested. If there are any errors then attempt to fix them with human input. "

    # Create a unit test but do not attempt to fix the errors #
    # prompt = f"Create one test class as needed for each method reported by the test coverage tool. Use the local vector store to retrieve information on the method, its class and its package. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created the test class should be saved to disk using an appropriate file name within `{args.data_path}`, and then tested. If there are any errors then explain them but do not attempt to fix them."

    # Test prompts for running specific tools! ##
    # prompt = "Run the test suite tool and report errors but do not fix them."
    # prompt = "Return classes and methods that require additional testing."

    agent.run_agent(prompt)
