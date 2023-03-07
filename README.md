# AI-Gui
AI-Gui is a simple desktop application that allows users to ask questions and receive answers using the OpenAI GPT-3 API. This project was built using Python and PySimpleGUI.

## Features
- Users can ask questions and receive answers using the OpenAI GPT-3 API.
- The application saves the user's chat history in a SQLite database.
- The application provides the user with the option to copy the response to the clipboard.

## Requirements
- Python 3.6+
- PySimpleGUI
- OpenAI API Key [https://platform.openai.com/account/api-keys]
- sqlite3
- requests 
- atexit
- os

## Installation
1. Clone the repository.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Replace `input-openai-api-keys-in-here` in line 43 with your OpenAI API key
4. Run `python main.py` to start the application.

## Usage
1. Type your question in the input field and click the "Send" button or press enter.
2. The application will process the question using the OpenAI GPT-3 API and display the response in the output field.
3. The application will save the user's chat history in a SQLite database.
4. The application provides the user with the option to copy the response to the clipboard.

## License
AI-Gui is licensed under the GNU Public License V3. See [LICENSE](https://github.com/wildybytes/AI-Gui/blob/main/LICENSE) for more information.
