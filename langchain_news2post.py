import json
from pathlib import Path
import shutil
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

model = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    api_key="api_key"
)


def generate_messages_from_files(folder_path):
    messages = []
    waiting_path = folder_path / 'waiting'
    processed_path = folder_path / 'processed'
    processed_path.mkdir(exist_ok=True)

    for file_path in waiting_path.glob('*.json'):
        with file_path.open('r', encoding='utf-8') as file:
            item = json.load(file)
            message = [
                SystemMessage(
                    content="Please summarize the following article. The output language should match the input "
                            "language. The output should be divided into multiple sections, with a minimum of 1 "
                            "section and a maximum of 6 sections, depending on the length and content of the article. "
                            "Each section should cover one main topic of the article. Please present it in the "
                            "following structure: [{\"heading\": \"...\", \"text\": \"...\"}, ...]"),
                HumanMessage(content=f"the article title: {item['title']}"),
                HumanMessage(content=f"the article content: {item['main_content']}")
            ]
            messages.append((message, file_path))

    return messages


def process_files(folder_path):
    messages = generate_messages_from_files(folder_path)
    processed_path = folder_path / 'processed'
    output_path = folder_path / 'output'
    output_path.mkdir(exist_ok=True)
    for message, file_path in messages:
        result = model.invoke(message)
        response_message = parser.invoke(result)
        output_file = output_path / file_path.name
        with output_file.open('w', encoding='utf-8') as file:
            try:
                response_json = json.loads(response_message)
            except json.JSONDecodeError as e:
                response_json = {
                    "error": "Invalid JSON response",
                    "response": response_message,
                    "details": str(e)
                }

            json.dump(response_json, file, ensure_ascii=False, indent=4)
        shutil.move(str(file_path), str(processed_path / file_path.name))


if __name__ == "__main__":
    folder_path = Path('../urls/langchain')
    process_files(folder_path)
