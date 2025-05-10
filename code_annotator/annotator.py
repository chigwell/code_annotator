import os
import re
import sys
import argparse
import logging # Added logging

from llmatch_messages import llmatch
from langchain_llm7 import ChatLLM7
from langchain_core.messages import HumanMessage, SystemMessage

# --- Logging Configuration ---
# Configure logging to output to console with a specific format and level
# You can customize the level (e.g., logging.DEBUG, logging.WARNING) and format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) # Ensure logs go to stdout
    ]
)
# --- End Logging Configuration ---

def get_annotated_code_from_llm(
    file_content: str,
    llm_temperature: float,
    llm_top_p: float,
    llm_max_tokens: int,
    custom_instruction: str = ""
) -> str | None:
    """
    Gets code annotations from an LLM using llmatch.

    Args:
        file_content: The Python code content to annotate.
        llm_temperature: Temperature for the LLM.
        llm_top_p: Top_p for the LLM.
        llm_max_tokens: Max tokens for the LLM response.
        custom_instruction: Specific user instructions for commenting.

    Returns:
        The annotated code as a string, or None if an error occurred.
    """

    # Initialize the LLM.
    try:
        llm = ChatLLM7(
            temperature=llm_temperature,
            top_p=llm_top_p,
            max_tokens=llm_max_tokens
        )
    except Exception as e:
        logging.error(f"Error initializing ChatLLM7: {e}")
        logging.error("Please ensure langchain_llm7 is installed and configured correctly.")
        logging.error("ChatLLM7 might not accept temperature, top_p, max_tokens directly in constructor.")
        logging.error("You may need to configure it via environment variables or other means.")
        return None

    system_prompt_content = (
        "You are a helpful code assistant. Your primary function is to add inline comments to Python code. "
        "You MUST return the complete, updated Python code block with your comments added. "
        "The code should be enclosed in a single markdown code block starting with ```python and ending with ```. "
        "DO NOT include any other text, explanations, apologies, or placeholders outside of this code block. "
        "ONLY THE MODIFIED CODE BLOCK IS REQUIRED."
    )
    if custom_instruction:
        system_prompt_content += f"\nFollow this specific instruction for commenting: {custom_instruction}"

    human_prompt_content = f"Please add comments to the following Python code:\n```python\n{file_content}\n```"

    messages = [
        SystemMessage(content=system_prompt_content),
        HumanMessage(content=human_prompt_content)
    ]

    code_extraction_pattern = r"```python\s*(.*?)\s*```"

    logging.info("Sending request to LLM via llmatch...")
    response_data = llmatch(
        llm=llm,
        messages=messages,
        pattern=code_extraction_pattern,
        verbose=False # Set to True or configure llmatch logger if it uses logging
    )

    if response_data["success"] and response_data["extracted_data"]:
        annotated_code = response_data["extracted_data"][0].strip()
        logging.info("Successfully extracted annotated code.")
        return annotated_code
    else:
        logging.error("Error processing with llmatch or extracting data.")
        if response_data.get("error_message"):
            logging.error(f"LLMatch Error: {response_data['error_message']}")
        if response_data.get("final_content"):
            # Using a multi-line log for better readability of raw response
            logging.error("LLM's final (raw) response was:\n---\n%s\n---", response_data['final_content'])
        else:
            logging.warning("No final content available from LLM.")
        return None

def update_part_of_file(file_path: str, original_content: str, new_content: str):
    """
    Replaces a part of the file with new content.
    """
    if not original_content:
        logging.warning("Original content is empty, cannot replace. Writing new content directly.")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            logging.info(f"Wrote new content to file: {file_path}")
        except IOError as e:
            logging.error(f"IOError writing new content to {file_path}: {e}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            current_file_content = file.read()
    except IOError as e:
        logging.error(f"IOError reading from {file_path} for update: {e}")
        return


    if original_content not in current_file_content:
        logging.warning(f"The exact original content was not found in {file_path}.")
        logging.warning("This might happen if the file was changed after being read.")
        logging.warning("Attempting to overwrite the entire file with the new content.")
        updated_content = new_content # Overwrite all
    else:
        updated_content = current_file_content.replace(original_content, new_content)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        logging.info(f"Updated file: {file_path}")
    except IOError as e:
        logging.error(f"IOError writing updated content to {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Code Annotator using llmatch and ChatLLM7')
    parser.add_argument('file_path', type=str, help='Path to the Python file to annotate')
    parser.add_argument('--temperature', type=float, default=0.1, help='Temperature for the LLM completion')
    parser.add_argument('--top_p', type=float, default=1.0, help='Top_p for the LLM completion')
    parser.add_argument('--max_tokens', type=int, default=2048, help='Maximum tokens for the LLM completion')
    parser.add_argument('--instruction', type=str, default="", help='Optional specific instructions for the type of comments to add (e.g., "Explain complex logic only")')
    parser.add_argument('--log-level', type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging output level")

    args = parser.parse_args()

    # --- Update logging level based on argument ---
    # Get the numeric value of the log level string
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {args.log_level}')
    logging.getLogger().setLevel(numeric_level) # Set level for the root logger
    # --- End update logging level ---


    if not os.path.exists(args.file_path):
        logging.error(f"File not found: {args.file_path}")
        sys.exit(1)

    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            original_file_content = file.read()
    except Exception as e: # General exception for file reading
        logging.error(f"Error reading file {args.file_path}: {e}")
        sys.exit(1)

    if not original_file_content.strip():
        logging.info(f"File {args.file_path} is empty. Nothing to annotate.")
        sys.exit(0)

    logging.info(f"Annotating {args.file_path}...")
    new_annotated_code = get_annotated_code_from_llm(
        file_content=original_file_content,
        llm_temperature=args.temperature,
        llm_top_p=args.top_p,
        llm_max_tokens=args.max_tokens,
        custom_instruction=args.instruction
    )

    if new_annotated_code:
        if new_annotated_code.strip():
            update_part_of_file(args.file_path, original_file_content, new_annotated_code)
            logging.info("Annotation complete.")
        else:
            logging.error("LLM returned empty content after extraction. File not updated.")
            sys.exit(1)
    else:
        logging.error("Failed to get annotations. File not updated.")
        sys.exit(1)

if __name__ == '__main__':
    main()