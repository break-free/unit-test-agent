#!/usr/bin/env python3

import argparse
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
import os
from src.unit_test_agent.unit_test_agent import UnitTestAgent
import sys
import time


class bcolors:
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'


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

    # Create dummy code coverage output for agent to create tests
    returned_tests = [
        '{ file: "fineract/fineract-client/src/main/java/org/apache/fineract/client/util/Parts.java", class: "Parts", method: "fromFile" }'
        # '{ file: "fineract/fineract-client/src/main/java/org/apache/fineract/client/util/Calls.java", class: "Calls", method: "ok" }'
    ]

    # Finally create, the Agent
    agent = UnitTestAgent(llm, conversational_memory)

    # Variables for statistics
    start_all = time.time()
    all_agent_total_tokens = 0
    all_agent_prompt_tokens = 0
    all_agent_completion_tokens = 0
    all_agent_total_cost = 0

    for test in returned_tests:

        # Callback allows us to capture data about tokens used and expenditure
        with get_openai_callback() as cb:

            # Create a unit test and then attempt to fix the errors #
            prompt = (
                f"""Create a test class for this class and method: `{test}`. Use the local """
                f"""vector store to retrieve information on the method, class and package. If """
                f"""the vector store is empty, populate the vector store with code from the """
                f"""following directory '{args.data_path}'. Once created the test class should """
                f"""be saved to disk using an appropriate file name within `{args.data_path}`, """
                f"""and then tested. If there are any errors then attempt to fix them until """
                f"""resolved."""
            )

            # Run the agent and capture time statistics
            start_agent = time.time()
            agent.run_agent(prompt)
            end_agent = time.time()

            print(
                bcolors.BOLD + bcolors.RED + f"\nAgent Execution took: {end_agent - start_agent}"
            )
            print(
                f"""Agent Total Tokens: {cb.total_tokens}, """
                f"""Prompt Tokens: {cb.prompt_tokens}, """
                f"""Completion Tokens: {cb.completion_tokens}\n """
                f"""Total Cost (USD): ${cb.total_cost}""" + bcolors.END
            )

            all_agent_total_tokens += cb.total_tokens
            all_agent_prompt_tokens += cb.prompt_tokens
            all_agent_completion_tokens += cb.completion_tokens
            all_agent_total_cost += cb.total_cost

    end_all = time.time()

    print(bcolors.BOLD + bcolors.RED + f"All Execution took: {end_all - start_all} seconds.")
    print(
        f"""All Agents -> Total Tokens: {all_agent_total_tokens}, """
        f"""Prompt Tokens: {all_agent_prompt_tokens}, """
        f"""Completion Tokens: {all_agent_completion_tokens}\n """
        f"""All Agents -> Total Cost (USD): ${all_agent_total_cost}""" + bcolors.END
    )
