# InputWindowAi
This Python script creates a GUI for a conversational assistant using PyQt5. 
The assistant is powered by OpenAI's GPT-3 model. To use the script, you need to fill in your OpenAI API key and an assistant ID.
The script sets up the GUI layout, handles user input, and displays the assistant's responses. 
It uses a separate worker thread to ensure responsiveness. The GUI includes features like drag and drop, minimize and close buttons, and a GIF background.

pip install:
pip install PyQt5
pip install python-dotenv
pip install openai
pip install os

in the .env add:
OPENAI_API_KEY = "YOUR KEY"
AssID  = "ASSIST_ID"

Also:
Go to open ai, create an assistant / and key and copy it into .env
