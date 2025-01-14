import os
import time

from ollama import chat
from ollama import ChatResponse

from openai import OpenAI

TSS_HOST = "http://localhost:8880/v1"
# Using the default Ollama Host

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
    folder_path = input(f"Enter the folder path of your images (default: {default}): ").strip()
    if not folder_path:
        folder_path = default
    return folder_path

def write_text_to_file(file_path, text):
    """
    Writes the given text to a file at the specified path.

    Args:
    file_path (str): The path to the file where the text will be written.
    text (str): The text to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

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
def generate_audio(text, output_dir):
    client = OpenAI(
        base_url=TSS_HOST,
        api_key="not-needed"
    )

    response = client.audio.speech.create(
        model="kokoro", 
        voice="af_nicole", #single or multiple voicepack combo
        input=text,
        response_format="mp3"
    )
    response.stream_to_file(output_dir + "/output.mp3")

def time_remaining(elapsed_time, completed, total):
    """
    Estimates the remaining time based on the elapsed time, completed pages, and total pages.

    Args:
    elapsed_time (float): The time taken to process the completed pages (in seconds).
    completed (int): The number of pages that have been processed.
    total (int): The total number of pages to be processed.

    Returns:
    float: The estimated remaining time (in minutes).
    """
    if completed == 0:
        return float('inf')  # Avoid division by zero
    average_time_per_page = elapsed_time / completed
    remaining_pages = total - completed
    return (average_time_per_page * remaining_pages) / 60

if __name__ == "__main__":
    directory_path = ask_for_input_folder()
    image_files = find_image_files(directory_path)
    image_files.sort()
    all_pages = ''
    
    total_pages = len(image_files)
    start_time = time.time()

    for index, file in enumerate(image_files):
        print(f'Reading text from {file}')
        page = extract_text(file)
        
        write_text_to_file(file + "_extracted.txt", page)
        all_pages += page
        
        elapsed_time = time.time() - start_time
        remaining_time = time_remaining(elapsed_time, index + 1, total_pages)
        
        print(f'Page {index + 1}/{total_pages} processed. Estimated remaining time: {remaining_time:.2f} minutes')

    print('Generating audio... (Just on moment)')
    generate_audio(all_pages, directory_path)
    print('Done :) Happy reading / listening!')