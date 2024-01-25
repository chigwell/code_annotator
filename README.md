[![PyPI version](https://badge.fury.io/py/code_annotator.svg)](https://badge.fury.io/py/code_annotator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/code_annotator)](https://pepy.tech/project/code_annotator)

# Code Annotator

`Code Annotator` is a Python package designed to automatically add comments to source code using the Mistral AI API. It enables users to quickly obtain comprehensive, context-aware comments throughout their code, facilitating better understanding and readability.

## Installation

To install `Code Annotator`, you can use pip:

```bash
pip install code_annotator
```

## Usage

### As a Command Line Tool

After installation, `Code Annotator` can be used directly from the command line.

Example:

```bash
code-annotator <api_token> <model_name> <file_path> [--temperature] [--top_p] [--max_tokens]
```

- `api_token`: Your Mistral API token.
- `model_name`: The name of the Mistral model to use.
- `file_path`: The path to the source code file you want to annotate.
- `temperature` (optional): The temperature parameter for the AI model.
- `top_p` (optional): The top_p parameter for the AI model.
- `max_tokens` (optional): The maximum number of tokens for the AI model to generate.

### Customizing Your Annotations

You can customize the behavior of `Code Annotator` by adjusting the optional command-line parameters, such as the temperature, top_p, max_tokens, etc., to fit the specific needs of your code or to tweak the behavior of the Mistral model.

## Output Example

When you run `Code Annotator`, it processes your source code file and adds insightful, context-aware comments to the code. Here is an example of the annotated code output:

```python
# Example of annotated code
def example_function(param1, param2):
    # This function performs a calculation using param1 and param2
    result = param1 + param2
    return result
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/chigwell/code_annotator/issues).

## License

[MIT](https://choosealicense.com/licenses/mit/)
