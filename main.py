# ----------------------------------------------------------------------------
#  Name         : AI-Gui
#  Desc         : AI-Gui is a program to make using OpenAI easier without 
#                 having to open the website.
#  Author       : Wildy Sheverando [Wildy8283]
#  Date         : 07-03-2023
#  License      : GNU General Public License V3
#  License Link : https://raw.githubusercontent.com/wildy8283/lcn/main/gplv3
# ----------------------------------------------------------------------------

# >> Import Requirement library
import os
import requests
import sqlite3
import atexit
import PySimpleGUI as sg

# >> Set themes to lightgrey1
sg.theme('LightGrey1')

# >> set path for logo and icon
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')

# >> set application icon
sg.set_global_icon(icon_path)

# >> connect to database and create a new database if it doesn't exist
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat_history
             (input text, output text)''')
conn.commit()

# >> set max chat history to be saved
MAX_HISTORY = 10
layout = [
    [sg.Multiline(size=(200, 19.4), key='-OUTPUT-', font=('Courier New', 14), disabled=True, enable_events=True)],
    [sg.Multiline(size=(200, 6), key='-INPUT-', font=('Courier New', 14), enter_submits=False)],
    [sg.Button('Send', size=(10, 2), bind_return_key=True), sg.Button('Copy', key='-COPY-', size=(10, 2), disabled=True)]
]
window = sg.Window('AI-Gui - 1.0.0 | WildyBytes', layout, size=(1000, 600), icon=icon_path)
url = 'https://api.openai.com/v1/completions'
headers = {'Authorization': 'Bearer input-openai-api-keys-in-here', "Content-Type": "application/json"}

# >> Create function for exit_handler and run atextit to handle the function start
def exit_handler():
    os.remove('database.db')
atexit.register(exit_handler)

# >> Run GUI event loop
while True:
    # >> Create event from window read
    event, values = window.read()

    # >> Close window if 'X' is clicked
    if event == sg.WIN_CLOSED:
        break

    # >> Process user input
    if event == 'Send':
        # >> Check if input is not empty
        if values['-INPUT-']:
            # >> Clean and prepare input for API request
            question = values['-INPUT-']
            question2 = question
            question = question.replace('\\\\', '\\\\\\\\')
            question = question.replace('\\n', '\\\\n')

            # >> Check if input length is valid
            if len(question.split('\n')) > 200:
                sg.popup('Maximum question length is 200!')
            else:
                # >> Get the latest chat history from the database
                c.execute("SELECT * FROM chat_history ORDER BY rowid DESC LIMIT 1")
                prev_input_output = c.fetchone()

                # >> Use previous 2 responses as prompt if they exist
                prompt = question
                prompts = ''
                if prev_input_output:
                    prev_input, prev_output = prev_input_output
                    prompt = f'{prev_input}\n{question}'

                    # >> Retrieve previous questions from database
                    questions = [prev_input]
                    for row in c.execute("SELECT * FROM chat_history ORDER BY rowid DESC LIMIT ?", (MAX_HISTORY,)):
                        questions.append(row[0])
                    questions = questions[::-1]
                    if len(questions) >= 2:
                        for i in range(len(questions) - 1):
                            prompts = f"\n\nHistory: {questions[i]}\n\n"

                # >> Set prompt2
                prompt2 = f"{prompts}\n\nQuestion: {question}\n\nAnswer without 'Answer:' or 'Jawaban:'\n"            
                data = {'model': 'text-davinci-003', 'prompt': prompt2, 'temperature': 0, 'max_tokens': 2048, 'top_p': 1, 'frequency_penalty': 0.3, 'presence_penalty': 0}
                try:
                    response = requests.post(url, headers=headers, json=data)
                    try:
                        result = response.json().get('choices')[0]['text'].strip()
                    except:
                        result = "Sorry, AI-Gui is unable to process your question because database queue is full.\n\nYou can remove files database.db to resolv this problem\n"
                    window['-OUTPUT-'].update(f"+> Question: \n{question2}\n\n+> Answer: \n{result}")
                    window['-INPUT-'].update('')
                    window['-COPY-'].update(disabled=False)
                    c.execute("INSERT INTO chat_history VALUES (?, ?)", (question2, result))
                    conn.commit()
                except requests.exceptions.ConnectionError:
                    sg.popup('No Internet Connection\n')
        else:
            sg.popup('Input question and try again !')

    if event == '-INPUT-' and '\n' in values['-INPUT-']:
        question = values['-INPUT-'].replace('\n', '\n')
        window['-INPUT-'].update(question + '\n')

    if event == '-INPUT-' and values['-INPUT-'].endswith(('\n', '\r\n')) and 'Shift' in values['_keychar']:
        question = values['-INPUT-'][:-1] + '\n'
        window['-INPUT-'].update(question)

    if event == '-OUTPUT-' and 'Control' in values['_keychar'] and 'c' in values['_keychar']:
        window['-OUTPUT-'].Widget.event_generate('<Control-C>')

    if event == '-COPY-':
        sg.clipboard_set(result)

# >> Close Database and PyAutoGUI
window.close()
conn.close()
