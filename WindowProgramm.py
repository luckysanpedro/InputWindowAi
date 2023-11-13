from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QThread
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMovie
import os
import time

#import assistant file:
import AssistantConversation
#Assistant conversation utils:
from dotenv import load_dotenv
from openai import OpenAI
from dotenv import load_dotenv
# Load your OpenAI API key
load_dotenv()
client = OpenAI()
#for the assistant to work:
initial_message = "Hello."
assistant_id = os.getenv('AssID')
thread = None
user_input = "" 

#this class manages what happens when the user hits enter in the input field:
class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        # Call the main function from AssistantConversation and get the result
        result = AssistantConversation.main(self.user_input)
        # Emit the result when the function is finished
        self.finished.emit(result)


# Define the input path for the GIF in the background
input_path = "C:/Users/julia_m2vnlyv/OneDrive/Desktop/InputWindowAi/hamsterbackground"
#to accept control+enter as a new line:
class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None, assistant_window=None):
        super().__init__(parent)
        self.assistant_window = assistant_window

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.insertPlainText("\n")
        elif event.key() == Qt.Key_Return and not event.modifiers():
            self.assistant_window.on_enter()
        else:
            super().keyPressEvent(event)

class AssistantWindow(QWidget):
    user_input_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        w = 550
        h = 350

        # main window
        self.resize(w, h)
        # remove frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        # make the main window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # round widget
        self.round_widget = QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgb(10, 10, 10);
            border-radius: 30px;
            """
        )

        self.layout = QVBoxLayout(self.round_widget)

        # Set the background as a gif image
        self.movie = QMovie(input_path)
        self.background_label = QLabel(self.round_widget)
        self.background_label.setMovie(self.movie)
        self.background_label.setAlignment(Qt.AlignCenter)  # Center the GIF
        self.background_label.setScaledContents(True)  # Resize the GIF to fit the QLabel
        self.background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow the label to expand
        self.background_label.setGeometry(10, 10, w-20, h-20)  # Set the geometry of the background_label to be slightly smaller than the round_widget
        self.movie.start()

        # Create a new layout for the other widgets
        self.widget_layout = QVBoxLayout()
        self.layout.addLayout(self.widget_layout)

        # Create a layout for the input label and box
        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)

        # Add a spacer to the left of the input label
        self.input_layout.addStretch()

        # Add a QLabel widget for Input
        self.input_label = QLabel("Input")
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_label.setFrameStyle(QLabel.Panel | QLabel.Raised)
        self.input_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Set the font size
        font = self.input_label.font()
        font.setPointSize(font.pointSize() + 2)
        self.input_label.setFont(font)

        # Set the margins
        self.input_label.setContentsMargins(10, 0, 10, 0)  # Add 10px of space on the left and right

        # Set the style sheet to make the edges rounded and font color white
        self.input_label.setStyleSheet("""
            border-radius: 10px;
            color: white;
        """)

        # Add the input label to the input layout
        self.input_layout.addWidget(self.input_label)

        # Add a spacer to the right of the input label
        self.input_layout.addStretch()

        self.input_field = CustomTextEdit(assistant_window=self)
        self.input_field.setStyleSheet("""
        border-radius: 10px;
        background-color: rgba(200, 200, 255, 0.9);
        border: 1px solid black;
        """)
        self.input_field.textChanged.connect(self.adjust_input_field_height)
        #define the size of the input field:
        self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.input_field.setFixedHeight(30)
        # Add the input field to the main layout
        self.layout.addWidget(self.input_field)



         # Enable drag and drop for this widget
        self.setAcceptDrops(True)
    
        # Create a layout for the drag and drop label
        self.drag_and_drop_layout = QHBoxLayout()
        self.layout.addLayout(self.drag_and_drop_layout)

        # Add a stretch to the left of the drag and drop label
        self.drag_and_drop_layout.addStretch()

        # Add a QLabel widget for drag and drop
        self.drag_and_drop_label = QLabel("Drag&Drop")
        self.drag_and_drop_label.setFrameStyle(QLabel.Panel | QLabel.Raised)
        self.drag_and_drop_label.setStyleSheet("""
            background-color: rgba(50, 50, 50, 1);
            color: white;
            border: 1px solid black;
            border-radius: 10px;
        """)  # Add a border to the drag and drop field
        self.drag_and_drop_label.setMaximumHeight(40)  # Limit the height of the drag and drop field

        # Set the font size to match the "Input" label
        font = self.input_label.font()
        self.drag_and_drop_label.setFont(font)

        # Set the size policy to match the "Input" label
        self.drag_and_drop_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add the drag and drop label to the drag and drop layout
        self.drag_and_drop_layout.addWidget(self.drag_and_drop_label)

        # Add a stretch to the right of the drag and drop label
        self.drag_and_drop_layout.addStretch()


        # Create a layout for the output label and box
        self.output_layout = QVBoxLayout()
        self.layout.addLayout(self.output_layout)

        # Add a QLabel widget for Output
        self.output_label = QLabel("Output")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setFrameStyle(QLabel.Panel | QLabel.Raised)
        self.output_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Set the font size
        font = self.output_label.font()
        font.setPointSize(font.pointSize() + 2)
        self.output_label.setFont(font)

        # Set the margins
        self.output_layout.setSpacing(0)
        self.output_label.setContentsMargins(10, 0, 10, 0)  # Add 10px of space on the left and right

        # Set the style sheet to make the edges rounded
        self.output_label.setStyleSheet("""
            border-radius: 10px;
            color: white;
        """)

        # Add the output label to the output layout
        self.output_layout.addWidget(self.output_label, alignment=Qt.AlignCenter)

        # Add a QTextEdit widget to display output text
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)  # Make the output field read-only
        self.output_field.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid black;
            border-radius: 20px;
        """)  # Add a border to the output field
        self.output_field.setMaximumHeight(190)  # Limit the maximum height of the output field
        self.output_field.setMinimumHeight(60)  # Set the initial height of the output field

        # Add the output field to the output layout
        self.output_layout.addWidget(self.output_field)


        # Add minimize and close buttons
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.minimize_button = QPushButton("Minimize")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("""
            background-color: rgba(55, 255, 255, 0.8);
            border-radius: 3px;
        """)  
        # Add a solid background to the minimize button
        self.button_layout.addWidget(self.minimize_button)
        self.button_layout.addStretch()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            background-color: rgba(55, 255, 255, 0.8);
            border-radius: 3px;
        """)  # Add a solid background to the close button
        self.button_layout.addWidget(self.close_button)

        #this is for moving the whole window around on the screen:
        # Add these lines to initialize the position
        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        if self.background_label.geometry().contains(event.pos()):
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.background_label.geometry().contains(event.pos()):
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    #this is for the drag and drop functionality:
    # Override the dragEnterEvent method
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():  # If the drag event contains URLs (file paths)
            event.accept()  # Accept the drag event
        else:
            event.ignore()  # Ignore the drag event
    # Override the dropEvent method
    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()  # Get the file path
        self.input_field.setText(file_path)  # Set the file path as the input field text


    # for the optiic of the input field:
    def adjust_input_field_height(self):
        num_lines = len(self.input_field.toPlainText().split('\n'))
        new_height = min(10 + num_lines * 20, 60)
        self.input_field.setFixedHeight(new_height)
    # add functionality to add a new line when the user hits ctrl+enter:
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.input_field.insert("\n")
        else:
            super().keyPressEvent(event)


#what is displayed in the output field:
    def display_output(self, assistant_message: str):
        self.output_field.append(assistant_message)  # Append the text to the output field
        # Adjust the height of the output field based on the number of text lines
        num_lines = len(self.output_field.toPlainText().split('\n'))
        new_height = min(60 + num_lines * 20, 190)
        self.output_field.setFixedHeight(new_height)


#when an input is entered / the user hits enter: (worker thread starts)
    def on_enter(self):
        user_input = self.input_field.toPlainText().rstrip("\n")
        if user_input.strip():
            self.input_field.clear()
            # Create a Worker instance
            self.worker = Worker(user_input)
            # Connect the finished signal to a slot
            self.worker.finished.connect(self.on_worker_finished)
            # Start the worker thread
            self.worker.start()
            # Display the user input in the output field
    def on_worker_finished(self, result):
        # Display the result in the output field
        self.display_output(result)

if __name__ == "__main__":
    app = QApplication([])

    # Create an instance of AssistantWindow
    assistant_window = AssistantWindow()

    # Display the initial message in the output window
    assistant_message = "Hello, I'm your Assistant."
    assistant_window.display_output(assistant_message)

    assistant_window.show()

    app.exec_()