[![PyPI version](https://badge.fury.io/py/code_annotator.svg)](https://badge.fury.io/py/code_annotator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/code_annotator)](https://pepy.tech/project/code_annotator)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# Code Annotator

`Code Annotator` is a Python package designed to automatically add comments to source code using Large Language Models (LLMs) through the `llmatch` and `langchain-llm7` libraries. It enables users to quickly obtain comprehensive, context-aware comments throughout their code, facilitating better understanding and readability.

## Installation

To install `Code Annotator`, you can use pip. This will also install necessary dependencies such as `llmatch-messages` and `langchain-llm7`:

```bash
pip install code_annotator
```

**Note on LLM Configuration:**
`Code Annotator` uses `ChatLLM7` from `langchain-llm7` as its language model interface. Depending on the specific LLM backend `ChatLLM7` is configured to use (e.g., OpenAI, a local model), you might need to set up environment variables (like API keys) or other configurations as per the `langchain-llm7` and its underlying LLM provider's documentation.

## Usage

### As a Command Line Tool

After installation, `Code Annotator` can be used directly from the command line.

Example:

```bash
code-annotator <file_path> [--temperature TEMP] [--top_p TOP_P] [--max_tokens MAX_TOKENS] [--instruction "INSTRUCTION"] [--log-level LEVEL]
```

**Arguments:**

* `<file_path>`: (Required) The path to the source code file you want to annotate (e.g., `my_script.py`).
* `--temperature` (optional): Sets the creativity of the LLM. Lower values (e.g., `0.1`) make the output more deterministic, higher values (e.g., `0.8`) make it more random. Default: `0.1`.
* `--top_p` (optional): Nucleus sampling parameter. The model considers the results of the tokens with top_p probability mass. Default: `1.0`.
* `--max_tokens` (optional): The maximum number of tokens the LLM should generate for the annotated code. Default: `2048`.
* `--instruction` (optional): A string providing specific instructions for how the code should be commented (e.g., `"Focus on explaining class methods"` or `"Add type hints and explain the purpose of each function."`). Default: `""`.
* `--log-level` (optional): Set the logging output level. Choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default: `INFO`.

**Example Invocation:**

```bash
code-annotator your_code.py --temperature 0.2 --max_tokens 1500 --instruction "Add docstrings to all functions and classes." --log-level DEBUG
```

### Customizing Your Annotations

You can customize the behavior of `Code Annotator` by:
* Adjusting the LLM parameters: `temperature`, `top_p`, and `max_tokens` to control the style and length of the generated comments.
* Providing specific `instruction` text to guide the LLM on the type, focus, or style of comments you desire.
* Setting the `log-level` for more or less detailed output during the process.

## Output Example

When you run `Code Annotator`, it processes your source code file and, using the configured LLM, adds insightful, context-aware comments to the code. The original file is then updated with this new, commented version.

```python
# Example of input code:
# def example_function(param1, param2):
#     result = param1 + param2
#     return result

# Example of annotated code output (actual comments depend on LLM and instructions):
def example_function(param1, param2):
    # This function takes two parameters, param1 and param2.
    # It performs an addition operation on these two parameters.
    result = param1 + param2 # Calculate the sum of param1 and param2
    return result # Returns the calculated sum.
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/chigwell/code_annotator/issues) (assuming this is still the correct link).

## License

[MIT](https://choosealicense.com/licenses/mit/)