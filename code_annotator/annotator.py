import sys
import os
import argparse
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def get_annotations_from_mistral(api_token, model_name, file_content, temperature, top_p, max_tokens, instruction=""):
    if instruction:
        instruction = f"{instruction}\n"
    instruction = "ADD COMMENTS TO THIS CODE\nPROVIDE ONLY FULL UPDATED CODE WITH COMMENTS\nDO NOT PROVIDE PLACEHOLDERS IN THE RESPONSE.\n" + instruction

    formatted_content = f"```python\n{file_content}\n```"

    client = MistralClient(api_key=api_token)

    messages = [
        ChatMessage(role="user", content=instruction + formatted_content)
    ]

    chat_response = client.chat(
        model=model_name,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    completion = chat_response.choices[0].message.content if chat_response.choices else ""
    code = extract_code_from_response(completion)
    return code

def extract_code_from_response(response_text):
    start_marker = "```"
    end_marker = "```"
    start_idx = response_text.find(start_marker)

    if start_idx != -1:
        end_of_start_marker_idx = response_text.find('\n', start_idx) + 1
        end_idx = response_text.find(end_marker, end_of_start_marker_idx)
        if end_idx != -1:
            return response_text[end_of_start_marker_idx:end_idx].strip()

    return response_text

def update_part_of_file(file_path, original_content, new_content):
    with open(file_path, 'r') as file:
        content = file.read()

    updated_content = content.replace(original_content, new_content)

    with open(file_path, 'w') as file:
        file.write(updated_content)

    print(f"Updated part of file: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Code Annotator using Mistral API')
    parser.add_argument('api_token', type=str, help='Mistral API token')
    parser.add_argument('model_name', type=str, help='Model name to use')
    parser.add_argument('file_path', type=str, help='Path to the file to annotate')
    parser.add_argument('--temperature', type=float, default=0.1, help='Temperature for the completion')
    parser.add_argument('--top_p', type=float, default=1, help='Top p for the completion')
    parser.add_argument('--max_tokens', type=int, default=1000, help='Maximum tokens for the completion')
    parser.add_argument('--instruction', type=str, default="", help='Type of comment to add')

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"File not found: {args.file_path}")
        sys.exit(1)

    with open(args.file_path, 'r') as file:
        file_content = file.read()

    new_content = get_annotations_from_mistral(args.api_token, args.model_name, file_content, args.temperature, args.top_p, args.max_tokens, args.instruction)
    update_part_of_file(args.file_path, file_content, new_content)

if __name__ == '__main__':
    main()
