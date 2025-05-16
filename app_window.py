import os
import platform
import subprocess
import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMenu, \
    QMenuBar, QAction, QStyleFactory


class AppWindow(QMainWindow):

    def __init__(self, Main):
        super().__init__()

        # Master
        self.Main = Main
        self.grid_size = self.set_grid_size()
        self.button_size = 40
        self.in_a_row = 5
        self.active_player_1 = True
        self.player_1_name = "Player 1"
        self.player_2_name = "Player 2"
        self.count = 0
        self.player_1_score = 0
        self.player_2_score = 0

        # Menu
        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("File")
        self.about_menu = QMenu("About")
        self.exit_action = QAction("Exit")
        self.help_action = QAction("Help")
        self.about_action = QAction("About")
        self.restart_action = QAction("Restart")
        self.new_game_action = QAction("New game")

        # Geometry
        self.window_width = int(self.grid_size * self.button_size)
        self.window_height = int(self.grid_size * self.button_size + 70)
        self.monitor = QGuiApplication.primaryScreen().geometry()

        # Layout
        self.central_widget = QWidget()
        self.h_box_info = QHBoxLayout()
        self.h_box_score = QHBoxLayout()
        self.h_box_spacer = QHBoxLayout()
        self.h_box_grid = QHBoxLayout()
        self.h_box_status = QHBoxLayout()
        self.v_box = QVBoxLayout()
        self.grid_layout = QGridLayout()

        # Buttons, labels and other
        self.buttons: List[List[QPushButton]] = []
        self.restart_button = QPushButton("Play again")
        self.player_1_label = QLabel(f"🟡{self.player_1_name}")
        self.player_2_label = QLabel(f"    {self.player_2_name}")
        self.player_1_score_label = QLabel(f"        {self.player_1_score}")
        self.score_label = QLabel("Score")
        self.player_2_score_label = QLabel(f"{self.player_2_score}        ")
        self.player_2_score_label.setTextFormat(Qt.PlainText)
        self.game_info_label = QLabel(f"{self.in_a_row} in a row")
        self.status_label = QLabel("")
        self.icon = QIcon(self.resource_path("tic_tac_toe.png"))
        self.spacer_label = QLabel("")

        # Initializing UI
        self.initUI()

    def initUI(self):

        # Layout
        self.setCentralWidget(self.central_widget)
        self.h_box_grid.addStretch() # This adds a stretch to the left side of the grid
        self.h_box_grid.addLayout(self.grid_layout) # The grid between two stretches
        self.h_box_grid.addStretch() # This adds a stretch to the right side of the grid
        self.h_box_info.addWidget(self.player_1_label, alignment=Qt.AlignCenter)
        self.h_box_info.addWidget(self.game_info_label, alignment=Qt.AlignCenter)
        self.h_box_info.addWidget(self.player_2_label, alignment=Qt.AlignCenter)
        self.h_box_status.addWidget(self.status_label, alignment = Qt.AlignCenter)
        self.h_box_score.addWidget(self.player_1_score_label, alignment = Qt.AlignLeft)
        self.h_box_score.addWidget(self.score_label, alignment = Qt.AlignCenter)
        self.h_box_score.addWidget(self.player_2_score_label, alignment = Qt.AlignRight)
        self.h_box_spacer.addWidget(self.spacer_label)
        self.v_box.addLayout(self.h_box_info)
        self.v_box.addLayout(self.h_box_score)
        self.v_box.addLayout(self.h_box_spacer)
        self.v_box.addLayout(self.h_box_grid)
        self.v_box.addLayout(self.h_box_status)
        self.central_widget.setLayout(self.v_box)

        # Menu
        self.setMenuBar(self.menu_bar)
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.about_menu)
        self.file_menu.addAction(self.new_game_action)
        self.file_menu.addAction(self.restart_action)
        self.file_menu.addAction(self.exit_action)
        self.about_menu.addAction(self.help_action)
        self.about_menu.addAction(self.about_action)
        self.exit_action.triggered.connect(self.exit)
        self.restart_action.triggered.connect(self.restart)
        self.new_game_action.triggered.connect(self.new_game)
        self.help_action.triggered.connect(self.open_help)
        self.about_action.triggered.connect(self.open_about)

        # Geometry
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.v_box.setSpacing(0)
        self.v_box.setContentsMargins(0, 0, 0, 0)
        self.center_window()

        # Labels, buttons and other
        self.setWindowIcon(self.icon)
        self.restart_button.setObjectName("restartButton")
        self.restart_button.setStyle(QStyleFactory.create("Fusion"))
        self.player_1_label.setObjectName("player1Label")
        self.player_2_label.setObjectName("player2Label")
        self.setWindowTitle("Custom size TicTacToe by Peter Szepesi v0.8")
        self.restart_button.clicked.connect(self.play_again)
        self.player_1_score_label.setObjectName("player1ScoreLabel")
        self.score_label.setObjectName("scoreLabel")
        self.player_2_score_label.setObjectName("player2ScoreLabel")
        self.setStyleSheet("""
            QLabel{
                font-family: Bahnschrift;
                font-size: 30px;
            }

            QLabel#player1Label{
                color: red;
            }

            QLabel#player2Label{
                color: blue;
            }
            
            QLabel#player1ScoreLabel{
                color: red;
            }
            
            QLabel#player2ScoreLabel{
                color: blue;
            }
            
            QLabel#scoreLabel{
                color: green;
            }
            
            AppWindow{
                background-color: rgb(230, 230, 255);
            }
            
            QPushButton#restartButton{
                font-family: Bahnschrift;
                font-size: 23px;
            }
            
        """)

    def center_window(self):
        monitor_width = self.monitor.width()
        monitor_height = self.monitor.height()
        window_x = int((monitor_width - self.window_width) / 2)
        window_y = int((monitor_height - self.window_height) / 2)
        self.setGeometry(window_x, window_y, self.window_width, self.height())

    def create_buttons(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = QPushButton()
                button.setFixedSize(self.button_size, self.button_size)
                button.clicked.connect(self.on_button_clicked)
                button.setStyle(QStyleFactory.create("Fusion"))
                row.append(button)
            self.buttons.append(row)

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.grid_layout.addWidget(self.buttons[i][j], i, j)

    def set_grid_size(self):
        return int(15)

    def on_button_clicked(self):
        sender: QPushButton
        sender = self.sender()
        if self.active_player_1:
            sender.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
            sender.setText("X")
            sender.setEnabled(False)
            self.active_player_1 = False
            self.player_2_label.setText(f"🟡{self.player_2_name}")
            self.player_1_label.setText(f"    {self.player_1_name}")
        else:
            sender.setStyleSheet("color: blue; font-size: 20px; font-weight: bold;")
            sender.setText("O")
            sender.setEnabled(False)
            self.active_player_1 = True
            self.player_1_label.setText(f"🟡{self.player_1_name}")
            self.player_2_label.setText(f"    {self.player_2_name}")

        winner = self.check_win()
        # If the winner is known
        if winner != "N":
            letter = sender.text()
            # Displaying who won
            if letter == "X":
                self.status_label.setStyleSheet("color: red;")
                self.status_label.setText(f"{self.player_1_name} won!")
                self.player_1_score += 1
                self.player_1_score_label.setText(f"        {self.player_1_score}")
            else:
                self.status_label.setStyleSheet("color: blue;")
                self.status_label.setText(f"{self.player_2_name} won!")
                self.player_2_score += 1
                self.player_2_score_label.setText(f"{self.player_2_score}        ")
            self.h_box_status.addWidget(self.restart_button, alignment=Qt.AlignCenter)

            # Disable the buttons
            for i in range(0, len(self.buttons)):
                for j in range(0, len(self.buttons[i])):
                    self.buttons[i][j].setEnabled(False)

    def check_win(self):
        winner = ""

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].text() == "X":
                    winner = self.check_directions_win(i, j, "X")
                    if winner != "N": return "X"
                elif self.buttons[i][j].text() == "O":
                    winner = self.check_directions_win(i, j, "O")
                    if winner != "N": return "O"
        return "N"

    def check_directions_win(self, row, column, letter):

        direction = 0

        while direction <= 7:
            self.count = 0
            if direction == 0: # N
                # Checking the top of Y axis
                if row < self.in_a_row - 1:
                    direction = 2
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 1: # NE
                # Checking the top of Y axis
                if row < self.in_a_row - 1:
                    direction = 2
                    continue
                # Checking the right side of X axis
                if column > self.grid_size - self.in_a_row:
                    direction = 4
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 2: # E
                # Checking the right side of X axis
                if column > self.grid_size - self.in_a_row:
                    direction = 4
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 3: # SE
                # Checking the right side of X axis
                if column > self.grid_size - self.in_a_row:
                    direction = 4
                    continue
                # Checking the bottom of Y axis
                if row > self.grid_size - self.in_a_row:
                    direction = 6
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 4: # S
                # Checking the bottom of Y axis
                if row > self.grid_size - self.in_a_row:
                    direction = 6
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 5: # SW
                # Checking the bottom of Y axis
                if row > self.grid_size - self.in_a_row:
                    direction = 6
                    continue
                # Checking the left side of X axis
                if column < self.in_a_row - 1:
                    direction = 8
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 6: # W
                # Checking the left side of X axis
                if column < self.in_a_row - 1:
                    direction = 8
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1
            elif direction == 7: # NW
                # Checking the left side of X axis
                if column < self.in_a_row - 1:
                    direction = 8
                    continue
                if self.validate_win(direction, letter, row, column): return letter
                else: direction += 1

        return "N"

    def validate_win(self, direction, letter, row, column):

        if direction == 0:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i -= 1
        elif direction == 1:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i -= 1
                j += 1
        elif direction == 2:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                j += 1
        elif direction == 3:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i += 1
                j += 1
        elif direction == 4:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i += 1
        elif direction == 5:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i += 1
                j -= 1
        elif direction == 6:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                j -= 1
        elif direction == 7:
            i = row
            j = column
            for k in range(0, self.in_a_row):
                if self.buttons[i][j].text() == letter:
                    self.count += 1
                i -= 1
                j -= 1

        # If there is the desired amount in a row, color the tiles
        if self.count == self.in_a_row:
            if direction == 0:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i -= 1
            elif direction == 1:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i -= 1
                    j += 1
            elif direction == 2:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    j += 1
            elif direction == 3:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i += 1
                    j += 1
            elif direction == 4:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i += 1
            elif direction == 5:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i += 1
                    j -= 1
            elif direction == 6:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    j -= 1
            elif direction == 7:
                i = row
                j = column
                for k in range(0, self.in_a_row):
                    if letter == "X":
                        self.buttons[i][j].setStyleSheet("background-color: red;")
                    elif letter == "O":
                        self.buttons[i][j].setStyleSheet("background-color: blue;")
                    i -= 1
                    j -= 1

            return True
        else: return False

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path) # In case of exe return the absolute path
        else:
            return os.path.join(os.path.abspath("."), relative_path) # In case of IDE return the relative path

    # Menu related functions
    def exit(self):
        sys.exit(0)

    def play_again(self):
        self.active_player_1 = True
        self.player_1_label.setText(f"🟡{self.player_1_name}")
        self.player_2_label.setText(f"    {self.player_2_name}")
        self.h_box_status.removeWidget(self.restart_button)
        self.restart_button.setParent(None)
        self.status_label.setText("")
        for i in range(0, len(self.buttons)):
            for j in range(0, len(self.buttons[i])):
                self.buttons[i][j].setEnabled(True)
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyle(QStyleFactory.create("Fusion"))
                self.buttons[i][j].setStyleSheet("")

    def restart(self):
        self.active_player_1 = True
        self.player_1_label.setText(f"🟡{self.player_1_name}")
        self.player_2_label.setText(f"    {self.player_2_name}")
        self.h_box_status.removeWidget(self.restart_button)
        self.restart_button.setParent(None)
        self.status_label.setText("")
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_score_label.setText(f"        {self.player_1_score}")
        self.player_2_score_label.setText(f"{self.player_2_score}        ")
        for i in range(0, len(self.buttons)):
            for j in range(0, len(self.buttons[i])):
                self.buttons[i][j].setEnabled(True)
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyle(QStyleFactory.create("Fusion"))
                self.buttons[i][j].setStyleSheet("")

    def new_game(self):
        self.active_player_1 = True
        self.player_1_label.setText(f"🟡{self.player_1_name}")
        self.player_2_label.setText(f"    {self.player_2_name}")
        self.h_box_status.removeWidget(self.restart_button)
        self.restart_button.setParent(None)
        self.status_label.setText("")
        self.buttons: List[List[QPushButton]] = []
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_score_label.setText(f"        {self.player_1_score}")
        self.player_2_score_label.setText(f"{self.player_2_score}        ")
        self.hide()
        self.Main.welcome_w.show()

    # File opening methods ***********************************************************************************
    def open_help(self):
        help_file_path = self.resource_path("Help.txt")

        try:
            if platform.system() == "Windows":
                os.startfile(help_file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", help_file_path])
            else:
                subprocess.call(["xdg-open", help_file_path])

            with open(help_file_path, "r") as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("You don't have permission to open this file")
        except Exception as e:
            print(f"Something went wrong, error message : {e}")

    def open_about(self):
        about_file_path = self.resource_path("About.txt")

        try:
            if platform.system() == "Windows":
                os.startfile(about_file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", about_file_path])
            else:
                subprocess.call(["xdg-open", about_file_path])

            with open(about_file_path, "r") as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("You don't have permission to open this file")
        except Exception as e:
            print(f"Something went wrong, error message : {e}")
