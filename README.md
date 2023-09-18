# unit-test-agent

Autonomous agent that produces unit tests for Java code base.

## Description

The `unit_test_agent` package permits the creation of an autonomous agent that when given a code
base, will attempt to create unit tests based on the output of a test coverage tool. Uses Apache
Fineract however, could be applied to other Java code bases with minor adjustments.

The technologies used:

- **LangChain**: Provides the underlying libraries for agents, tools, prompts, memory, and indexes.
- **OpenJDK**: Provides the necessary libraries to compile Java code.
- **JUnit**: Provides the test suite.

Associated technologies to which this is tuned:

- **Apache Fineract**: Used for demonstration purposes, to replicate an expected financial
application. Technically any Java code base could be used however, the package is currently "tuned"
to this application.
- **OpenAI ChatGPT 4.0**: LangChain libraries are used to interact with the code base however, other
chat models could be utilized.
- **Chroma DB**: LangChain libraries are used to interact with this index/vector store. Other vector
stores could be used to achieve the same result

## Installation

Note these installation instructions assume you are running a Fedora Linux instance with `toolbox`
installed. For installation on other operating systems, follow the steps as executed in the build
script.

### Download and setup environment

To install and run the `demo.py` file first download the repository.

    git clone https://github.com/break-free/unit-test-agent.git

Once downloaded enter the directory and run the build script. Note you need an OpenAI API key to run
the build script; it will not run without one.

    cd unit-test-agent
    ./setup/build_unit-test-agent.sh $OPENAI_API_KEY

Once completed, enter the toolbox.

    toolbox enter unit-test-agent

### Setup Apache Fineract test suite

Prior to running the agent, ensure that you can run and build tests. First download the Apache
Fineract source code, setup the running of tests, and then return to the `unit-test-agent`
directory to run the script that executes the tests. The Apache Fineract code to be downloaded is
from a BreakFree repository, which was forked from the original at v1.8.4. Edits have been made to
ease testing and reduce test output.

	git clone https://github.com/break-free/fineract.git
	cd fineract
	docker run --name mariadb-10.8 -p 3306:3306 -e MARIADB_ROOT_PASSWORD#mysql -d mariadb:10.8
	./gradlew createDB -PdbName#fineract_tenants
	./gradlew createDB -PdbName#fineract_default
	./gradlew clean test

Once testing has been completed, you may remove the MariaDB container using the following command.

    docker rm -f mariadb-10.8

Finally, return to the `unit-test-agent` directory to test the `run_gradle.sh` script, which runs
the test suite.

    cd ..
    chmod +x ./src/run_gradle.sh
    ./src/run_gradle.sh

This should result in the tests running without errors.

> [!NOTE]
> Cucumber `*.feature` files have been removed, leaving only JUnit tests running. This was done on purpose to prevent sporadic errors (i.e., 1 in 4 test suite runs) from occurring. If additional Cucumber errors are encountered consider running the following command to remove any `*.feature` files:
>
> `find fineract/ -iname *.feature -exec rm '{}' \;`

## Run the Agent

Once setup, to run the agent use the following command (from the `unit-test-agent` directory):

    chmod +x demo.py
    ./demo.py

This will start the agent that attempts to generate a unit test, test, and then fix it (as
necessary). Only one test is generated using this file and it takes anywhere between four to ten
minutes (depending on the day). This test is generated consistently hence its use in
demonstrations.

> [!Note]
> The Agent uses the `fineract-client` directory by default to:
>
> - Populate the vector store.
> - Provide it with classes that require testing.
>
> Other code bases outside of this should be considered for experimentation only and are not
guaranteed to work as expected.

> [!Note]
> Currently only one test is created. To create two, uncomment the line within `returned_tests` to
> create one more. To create more than these two for demonstration purposes, then add more to the
> `returned_tests` list in `demo.py`. Make sure that these are tested prior to any demonstration
> with a client!

## Using the Agent

The `demo.py` is one way to use the agent. This can be extended and the enclosed prompt edited to
suit your requirements. The source code has been split up to reflect the BreakFree LLM model, and
can also be amended to reflect your requirements.

> [!CAUTION]
> Editing the prompts is the most likely option to extend this agent. It is important when doing so
> to be careful about phrasing and the terminology used. Consistency in terms and how they are used
> within prompts is critical for the agent to understand what tools it should use when.

## Credits

- The entire BreakFree team: for providing code, unique insights, and alternative paths of
progression; I stand on the shoulders of giants.
- https://github.com/langchain-ai/langchain[LangChain Project]: for creating an impressive
collection of libraries supporting interaction with and extending large language models; you guys
are awesome.
- https://github.com/apache/fineract[Apache Fineract]: for creating an excellent financial
application that we can use for testing agents.

## License

Refer to [the license](LICENSE).
