import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QInputDialog
import sqlite3

class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login/Register App")
        self.setGeometry(100, 100, 300, 200)

        self.initUI()

    def initUI(self):
        self.create_database()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def create_database(self):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')

        conn.commit()
        conn.close()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message_box("Error", "Please enter username and password.")
            return

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            self.show_message_box("Success", "Login successful!")
            self.show_main_menu()
        else:
            self.show_message_box("Error", "Invalid username or password.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message_box("Error", "Please enter username and password.")
            return

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self.show_message_box("Success", "Registration successful!")
        except sqlite3.IntegrityError:
            self.show_message_box("Error", "Username already exists.")

        conn.close()

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def show_main_menu(self):
        main_menu = QMessageBox()
        main_menu.setWindowTitle("Main Menu")
        main_menu.setText("Welcome to the main menu!")

        operations_button = main_menu.addButton("Operations", QMessageBox.YesRole)
        compare_button = main_menu.addButton("Compare", QMessageBox.NoRole)
        exit_button = main_menu.addButton("Exit", QMessageBox.RejectRole)

        main_menu.exec_()
        if main_menu.clickedButton() == operations_button:
            self.show_operations_menu()
        elif main_menu.clickedButton() == compare_button:
            self.show_compare_menu()
        elif main_menu.clickedButton() == exit_button:
            sys.exit()

    def show_operations_menu(self):
        operations_menu = QMessageBox()
        operations_menu.setWindowTitle("Operations Menu")
        operations_menu.setText("Welcome to the operations menu!")

        change_password_button = operations_menu.addButton("Change Password", QMessageBox.YesRole)
        back_button = operations_menu.addButton("Back", QMessageBox.NoRole)

        operations_menu.exec_()
        if operations_menu.clickedButton() == change_password_button:
            self.show_change_password_menu()

    def show_change_password_menu(self):
        change_password_menu = QMessageBox()
        change_password_menu.setWindowTitle("Change Password")
        change_password_menu.setText("Welcome to the change password menu!")

        old_password_input, ok1 = QInputDialog.getText(self, "Input", "Old Password:")
        new_password_input, ok2 = QInputDialog.getText(self, "Input", "New Password:")

        if ok1 and ok2:
            self.change_password(old_password_input, new_password_input)

    def change_password(self, old_password, new_password):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        username = self.username_input.text()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()

        if row is None:
            self.show_message_box("Error", "Invalid username.")
            return

        db_old_password = row[0]
        if db_old_password != old_password:
            self.show_message_box("Error", "Incorrect old password.")
            return

        c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit()

        conn.close()
        self.show_message_box("Success", "Password changed successfully!")

    def show_compare_menu(self):
        compare_menu = QMessageBox()
        compare_menu.setWindowTitle("Compare Menu")
        compare_menu.setText("Welcome to the compare menu!")

        vocal_similarity_button = compare_menu.addButton("Vocal Similarity", QMessageBox.ActionRole)
        consonant_similarity_button = compare_menu.addButton("Consonant Similarity", QMessageBox.ActionRole)
        back_button = compare_menu.addButton("Back", QMessageBox.NoRole)

        compare_menu.exec_()
        if compare_menu.clickedButton() == vocal_similarity_button:
            self.show_vocal_similarity()
        elif compare_menu.clickedButton() == consonant_similarity_button:
            self.show_consonant_similarity()

    def show_vocal_similarity(self):
        text1, ok1 = QInputDialog.getText(self, "Input", "1. Text:")
        text2, ok2 = QInputDialog.getText(self, "Input", "2. Text:")

        if ok1 and ok2:
            similarity = self.calculate_vocal_similarity(text1, text2)
            self.show_message_box("Similarity Result", f"Vocal similarity ratio: {similarity}")

    def calculate_vocal_similarity(self, text1, text2):
        vowels = set("aeıioöuü")
        vowel_count1 = sum(1 for char in text1.lower() if char in vowels)
        vowel_count2 = sum(1 for char in text2.lower() if char in vowels)
        total_chars1 = len(text1)
        total_chars2 = len(text2)
        vocal_similarity = (vowel_count1 + vowel_count2) / (total_chars1 + total_chars2)
        return vocal_similarity

    def show_consonant_similarity(self):
        text1, ok1 = QInputDialog.getText(self, "Input", "1. Text:")
        text2, ok2 = QInputDialog.getText(self, "Input", "2. Text:")

        if ok1 and ok2:
            similarity = self.calculate_consonant_similarity(text1, text2)
            self.show_message_box("Similarity Result", f"Consonant similarity ratio: {similarity}")

    def calculate_consonant_similarity(self, text1, text2):
        consonants = set("bcçdfgğhjklmnprsştvyz")
        consonant_count1 = sum(1 for char in text1.lower() if char in consonants)
        consonant_count2 = sum(1 for char in text2.lower() if char in consonants)
        total_chars1 = len(text1)
        total_chars2 = len(text2)
        consonant_similarity = (consonant_count1 + consonant_count2) / (total_chars1 + total_chars2)
        return consonant_similarity

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterApp()
    window.show()
    sys.exit(app.exec_())
