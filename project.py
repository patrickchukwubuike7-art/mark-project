

    # Mark Voice Assistant with GUI
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtCore import Qt
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia


# --- Enhanced and fixed class structure ---

class MarkAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mark Voice Assistant")
        self.setGeometry(100, 100, 900, 750)
        self.setFixedSize(700, 650)

        # --- Background layers ---
        # Solid black background
        self.bg_widget = QLabel(self)
        self.bg_widget.setGeometry(0, 0, 900, 750)
        self.bg_widget.setStyleSheet("background-color: black;")
        self.bg_widget.lower()

        # Animated GIF background
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 900, 750)
        self.movie = QMovie(r"C:/Users/HP/Desktop/gifloader (1).gif")
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self.bg_label.raise_()  # Ensure GIF is above black bg

        # --- Overlay widgets ---

        # Overlay widgets
        self.title_label = QLabel("Mark Voice Assistant", self)
        self.title_label.setFont(QFont("Arial", 28))
        self.title_label.setStyleSheet("color: white; background:black;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(60)

        self.output_box = QTextEdit(self)
        self.output_box.setFont(QFont("Arial", 16))
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("background: transparent; color: white; border: none;")
        self.output_box.setMinimumHeight(500)
        self.output_box.setMaximumHeight(600)

        from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
        self.input_line = QLineEdit(self)
        self.input_line.setFont(QFont("Arial", 16))
        self.input_line.setPlaceholderText("Type your command to Mark...")
        self.input_line.setStyleSheet("background: rgba(255,255,255,0.2); color: white; border-radius: 8px; padding: 8px;")
        self.input_line.setMinimumHeight(40)

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Arial", 16))
        self.send_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 8px; padding: 8px 24px;")
        self.send_button.setMinimumHeight(40)
        self.send_button.clicked.connect(self.send_text_command)

        self.listen_enabled = True
        self.toggle_listen_button = QPushButton("Disable Voice Listening", self)
        self.toggle_listen_button.setFont(QFont("Arial", 16))
        self.toggle_listen_button.setStyleSheet("background-color: #F44336; color: white; border-radius: 8px; padding: 8px 24px;")
        self.toggle_listen_button.setMinimumHeight(40)
        self.toggle_listen_button.clicked.connect(self.toggle_listening)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line, 3)
        input_layout.addWidget(self.send_button, 1)
        input_layout.addWidget(self.toggle_listen_button, 2)
        input_layout.setSpacing(20)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.output_box)
        layout.addLayout(input_layout)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)

       
    def toggle_listening(self):
        self.listen_enabled = not self.listen_enabled
        if self.listen_enabled:
            self.toggle_listen_button.setText("Disable Voice Listening")
            self.toggle_listen_button.setStyleSheet("background-color: #F44336; color: white; border-radius: 8px; padding: 4px 12px;")
            self.start_listening()
        else:
            self.toggle_listen_button.setText("Enable Voice Listening")
            self.toggle_listen_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 8px; padding: 4px 12px;")
    def send_text_command(self):
        user_text = self.input_line.text().strip()
        if user_text:
            self.input_line.clear()
            self.process_instruction(user_text)

    def talk(self, text):
        engine = pyttsx3.init('sapi5')
        engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)
        engine.say(text)
        engine.runAndWait()


    def input_instruction(self):
        recognizer = sr.Recognizer()
        instruction = ""
        try:
            with sr.Microphone() as source:
                self.output_box.append("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                instruction = recognizer.recognize_google(audio)
                instruction = instruction.lower()
                if "mark" in instruction:
                    self.output_box.append(f"Heard: {instruction}")
                    instruction = instruction.replace('mark', '').strip()
                    self.output_box.append(f"Command: {instruction}")
        except sr.UnknownValueError:
            self.output_box.append("Sorry, I did not understand that.")
            self.talk("Sorry, I did not understand that.")
        except sr.RequestError:
            self.output_box.append("Sorry, my speech service is down.")
            self.talk("Sorry, my speech service is down.")
        except Exception as e:
            self.output_box.append(f"Error: {e}")
            self.talk("An error occurred.")
        return instruction

    def process_instruction(self, instruction):
        if not instruction:
            return
        self.output_box.append(f"Instruction: {instruction}")
        print(f"Instruction: {instruction}")
        if "play" in instruction:
            import os
            song = instruction.replace('play', '').strip()
            self.talk("Playing " + song)
            self.output_box.append(f"Playing: {song}")
            # Try to play from user's Music folder first
            music_folder = os.path.join(os.path.expanduser('~'), 'Music')
            found = False
            for ext in ['.mp3', '.wav', '.aac', '.wma', '.m4a', '.flac']:
                local_path = os.path.join(music_folder, song + ext)
                if os.path.exists(local_path):
                    try:
                        if sys.platform == 'win32':
                            os.startfile(local_path)
                        else:
                            import subprocess
                            subprocess.Popen(['xdg-open', local_path])
                        self.output_box.append(f"Playing from PC: {local_path}")
                        found = True
                        break
                    except Exception as e:
                        self.output_box.append(f"Error playing local file: {e}")
                        break
            if not found:
                self.output_box.append("Not found locally, playing from YouTube...")
                pywhatkit.playonyt(song)
        elif 'time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            self.talk('Current time is ' + time)
            self.output_box.append(f"Current time is {time}")
        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            self.talk("Today's date is " + date)
            self.output_box.append(f"Today's date is {date}")
        elif 'how are you doing' in instruction:
            self.talk('I am fine, how about you?')
            self.output_box.append("I am fine, how about you?")
        elif 'what is your name' in instruction:
            self.talk('I am Mark, what can I do for you?')
            self.output_box.append("I am Mark, what can I do for you?")
        elif 'kedu ka i mere' in instruction:
            self.talk('I am fine, how about you?')
            self.output_box.append("I am fine, how about you?")
        elif 'kedu aha gi' in instruction:
            self.talk('I am Mark, what can I do for you?')
            self.output_box.append("I am Mark, what can I do for you?")
        elif 'who is' in instruction:
            human = instruction.replace('who is', '').strip()
        elif 'what is' in instruction:
            human = instruction.replace('what is', '').strip()
            try:
                info = wikipedia.summary(human, 1)
                print(info)
                self.talk(info)
                self.output_box.append(info)
            except Exception as e:
                self.output_box.append(f"Wikipedia summary error: {e}")
                # Try to fetch the page content as a fallback
                try:
                    page = wikipedia.page(human)
                    if page.content:
                        first_sentence = page.content.split('. ')[0] + '.'
                        self.talk(first_sentence)
                        self.output_box.append(first_sentence)
                    else:
                        self.talk("Sorry, I could not find information on that person.")
                        self.output_box.append("Sorry, I could not find information on that person.")
                except Exception as e2:
                    self.output_box.append(f"Wikipedia page error: {e2}")
                    self.talk("Sorry, I could not find information on that person.")
        else:
            self.talk('Please repeat your command.')
            self.output_box.append("Please repeat your command.")

        # After processing, listen again for voice commands if enabled
        if self.listen_enabled:
            self.start_listening()

    def start_listening(self):
        if not self.listen_enabled:
            return
        instruction = self.input_instruction()
        # Only process if not empty (avoid infinite loop on error)
        if instruction:
            self.process_instruction(instruction)

def main():
    app = QApplication(sys.argv)
    window = MarkAssistant()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()