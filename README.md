# Audio Book Reader

This project provides a simple script to convert an analog book (image) into an audiobook using AI technologies. The script processes images of book pages, extracts the text, and generates audio from the extracted text.

## Features

- **Image Processing**: Identify and process images of book pages.
- **Text Extraction**: Extract text from images using Optical Character Recognition (OCR).
- **Audio Generation**: Generate audio from the extracted text using AI.

## Requirements

- Python 3.x
- Required Python packages (install via `requirements.txt`):
  - `ollama`
  - `openai`

## Services

- Ollama:  
You can download Ollama from here https://ollama.com. I recommend the Docker version.

- OpenAi compatible TTS:  
Kokoro is a very strong TTS model. Remsky on GitHub build a RestAPI with Python [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI).

## Installation

1. Clone the repository:
   ```bash
   git clone https://code.mymiggi.de/Miggi/audiobook-reader.git
   cd book-to-audiobook
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place the images of book pages in a directory (default: `./test_input`).

2. Run the script:
   ```bash
   python main.py
   ```

3. The script will prompt you for the input folder. Press Enter to use the default `./test_input`.

4. The script will process the images, extract text, and generate an audio file from the text.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.