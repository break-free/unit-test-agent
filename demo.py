#!/usr/bin/env python3

import argparse
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
import os
from src.unit_test_agent.unit_test_agent import UnitTestAgent
import sys
import time

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
        model_name='gpt-4',
        max_retries=20
    )

    # initialize conversational memory using tokens
    conversational_memory = ConversationTokenBufferMemory(
        llm=llm,
        max_token_limit=3400,
        return_messages=True,
        verbose=True
    )

    agent = UnitTestAgent(llm, conversational_memory)

    returned_tests = [
        '{ file: "fineract/fineract-client/src/main/java/org/apache/fineract/client/util/Parts.java", class: "Parts", method: "fromFile" }',
        '{ file: "fineract/fineract-client/src/main/java/org/apache/fineract/client/util/Calls.java", class: "Calls", method: "ok" }',
        '[ file: "fineract/fineract-client/src/main/java/org/apache/fineract/client/util/CallFailedRuntimeException.java", class: "CallFailedRuntimeException", method: "message" ]'
    ]

    start_all = time.time()

    for test in returned_tests:

        # Create a unit test and then attempt to fix the errors #
        prompt = f"Create a test class for this class and method: `{test}`. Use the local vector store to retrieve information on the method, class and package. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created the test class should be saved to disk using an appropriate file name within `{args.data_path}`, and then tested. If there are any errors then attempt to fix them until resolved."

        start_agent = time.time()
        agent.run_agent(prompt)
        end_agent = time.time()
        print(f"Agent Execution took: {end_agent - start_agent}")

    end_all = time.time()
    print(f"All Agent Execution took: {end_all - start_all} seconds.")

    # A human in the loop prompt
    # prompt = f"Create one test class as needed for each method reported by the test coverage tool. Use the local vector store to retrieve information on the method, its class and its package as often as needed. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created, the test class should be saved to disk using an appropriate file name, checked by a human, and then tested. If there are any errors then attempt to fix them with human input. "

    # Create a unit test but do not attempt to fix the errors #
    # prompt = f"Create one test class as needed for each method reported by the test coverage tool. Use the local vector store to retrieve information on the method, its class and its package. If the vector store is empty, populate the vector store with code from the following directory '{args.data_path}'. Once created the test class should be saved to disk using an appropriate file name within `{args.data_path}`, and then tested. If there are any errors then explain them but do not attempt to fix them."

    # Test prompts for running specific tools! ##
    # prompt = "Run the test suite tool and report errors but do not fix them."
    # prompt = "Return classes and methods that require additional testing."
