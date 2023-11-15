from .window_programm import AssistantWindow, QApplication, assistant_message


app = QApplication([])

# Create an instance of AssistantWindow
assistant_window = AssistantWindow()

# Display the initial message in the output window
assistant_window.display_output(assistant_message)

assistant_window.show()

app.exec_()
