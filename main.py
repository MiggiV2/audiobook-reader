import os

from ollama import chat
from ollama import ChatResponse

from openai import OpenAI

def find_image_files(directory):
    """
    Recursively searches for .png, .jpeg, and .jpg files in the given directory and its subdirectories.

    Args:
    directory (str): The directory to search for image files.

    Returns:
    list: A list of paths to image files.
    """
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg')):
                image_files.append(os.path.join(root, file))
    return image_files

def ask_for_input_folder(default='./test_input'):
    """
    Prompts the user to input a folder path. Uses the default path if the user just presses enter.
    
    Args:
    default (str): The default folder path to use if the user doesn't provide input.
    
    Returns:
    str: The folder path provided by the user or the default path.
    """
    folder_path = input(f"Enter the folder path (default: {default}): ").strip()
    if not folder_path:
        folder_path = default
    return folder_path

# Ollama
def extract_text(file):
    response: ChatResponse = chat(model='llama3.2-vision', messages=[
    {
        'role': 'user',
        'content': 'Exctract the text from the image. Ingore the title and page number.',
        'images': [file]
    },
    ])
    return response.message.content

# Kokoro
def generate_audio(text):
    client = OpenAI(
        base_url="http://localhost:8880/v1",
        api_key="not-needed"
    )

    response = client.audio.speech.create(
        model="kokoro", 
        voice="af_nicole", #single or multiple voicepack combo
        input=text,
        response_format="mp3"
    )
    response.stream_to_file("output.mp3")

if __name__ == "__main__":
    directory_path = ask_for_input_folder()
    image_files = find_image_files(directory_path)
    image_files.sort()
    all_pages = ''

    for file in image_files:
        print('Reading text from ' + file)
        page = extract_text(file)
        print('Found ' + len(page.split()) + ' words!')
        all_pages += page

    generate_audio(all_pages)