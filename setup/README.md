A simple toolbox script that creates a containerized development environment where this repository's code can be built and run.

# Disclaimer

Refer to the master https://github.com/break-free/fineract-unit-tests-openai/blob/fix_use-token-counters/README.adoc[`README.adoc`] file for additional details.

# TODO

- [ ] **TODO:** Amend and then confirm that Windows installation works as expected.

---

## Fedora OS

1. Download the code from this repository from your root directory. Note this includes the test files under `training/tests`.

2. Get your OpenAI API key and add it to your environment.

    $ export OPENAI_API_KEY=<YOUR_KEY>

3. Enter the code repo directory and run the `toolbox` script. Note the requirement to add both your OPEN API key as well as an API secret.

    $ cd unit-test-agent
    $ setup/build_unit-test-agent.sh
    $ toolbox enter unit-test-agent

---

> **Warning**
> The windows portion of the documentation is not complete! Do not rely on it in its current state!

## Windows

To be completed ...
