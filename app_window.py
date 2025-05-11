import time
from typing import List

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Master
        self.grid_size = self.set_grid_size()
        self.button_size = 40
        self.in_a_row = 5
        self.active_player_1 = True
        self.player_1_name = "Player 1"
        self.player_2_name = "Player 2"
        self.count = 0

        # Geometry
        self.window_width = int(self.grid_size * self.button_size)
        self.window_height = int(self.grid_size * self.button_size + 70)
        self.monitor = QGuiApplication.primaryScreen().geometry()

        # Layout
        self.central_widget = QWidget()
        self.v_box = QVBoxLayout()
        self.grid = QGridLayout()
        self.h_box_info = QHBoxLayout()

        # Buttons, labels and other
        self.buttons: List[List[QPushButton]] = []
        self.player_1_label = QLabel(f"🟡{self.player_1_name}")
        self.player_2_label = QLabel(f"    {self.player_2_name}")
        self.game_info_label = QLabel(f"{self.in_a_row} in a row")

        # Initializing UI
        self.initUI()

    def initUI(self):

        # Layout
        self.setCentralWidget(self.central_widget)
        self.h_box_info.addWidget(self.player_1_label, alignment=Qt.AlignCenter)
        self.h_box_info.addWidget(self.game_info_label, alignment=Qt.AlignCenter)
        self.h_box_info.addWidget(self.player_2_label, alignment=Qt.AlignCenter)
        self.v_box.addLayout(self.h_box_info)
        self.v_box.addLayout(self.grid)
        self.central_widget.setLayout(self.v_box)

        # Geometry
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.v_box.setContentsMargins(0, 0, 0, 0)
        self.center_window()

        # Labels, buttons and other
        self.player_1_label.setObjectName("player1Label")
        self.player_2_label.setObjectName("player2Label")
        self.setWindowTitle("Custom size TicTacToe by Peter Szepesi")
        self.create_buttons()
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
            
        """)

    def center_window(self):
        self.setFixedWidth(self.window_width)
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
                row.append(button)
            self.buttons.append(row)

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.grid.addWidget(self.buttons[i][j], i, j)

    def set_grid_size(self):
        return int(15)

    def on_button_clicked(self):
        sender: QPushButton
        sender = self.sender()
        if self.active_player_1:
            sender.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
            sender.setText("X")
            sender.clicked.disconnect()
            self.active_player_1 = False
            self.player_2_label.setText(f"🟡{self.player_2_name}")
            self.player_1_label.setText(f"    {self.player_1_name}")
        else:
            sender.setStyleSheet("color: blue; font-size: 20px; font-weight: bold;")
            sender.setText("O")
            sender.clicked.disconnect()
            self.active_player_1 = True
            self.player_1_label.setText(f"🟡{self.player_1_name}")
            self.player_2_label.setText(f"    {self.player_2_name}")

        self.check_win()

    def check_win(self):
        start = time.time_ns()

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].text() == "X":
                    self.check_directions_win(i, j, "X")
                elif self.buttons[i][j].text() == "O":
                    self.check_directions_win(i, j, "O")

        print(f"Duration : {time.time_ns() - start}ns")

    def check_directions_win(self, row, column, letter):

        direction = 0

        while direction <= 7:
            self.count = 0
            if direction == 0: # N
                # Checking the top of Y axis
                if row < self.in_a_row - 1:
                    direction = 2
                    continue
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
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
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
                else: direction += 1
            elif direction == 2: # E
                # Checking the right side of X axis
                if column > self.grid_size - self.in_a_row:
                    direction = 4
                    continue
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
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
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
                else: direction += 1
            elif direction == 4: # S
                # Checking the bottom of Y axis
                if row > self.grid_size - self.in_a_row:
                    direction = 6
                    continue
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
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
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
                else: direction += 1
            elif direction == 6: # W
                # Checking the left side of X axis
                if column < self.in_a_row - 1:
                    direction = 8
                    continue
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
                else: direction += 1
            elif direction == 7: # NW
                # Checking the left side of X axis
                if column < self.in_a_row - 1:
                    direction = 8
                    continue
                if self.validate_win(direction, letter, row, column): print(f"{letter} won")
                else: direction += 1

        print("EOF")

    def validate_win(self, direction, letter, row, column):
        pass
