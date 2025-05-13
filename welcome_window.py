from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox


class WelcomeWindow(QWidget):

    def __init__(self, app_window):
        super().__init__()

        # Master
        from app_window import AppWindow
        self.app_window: AppWindow = app_window

        # Geometry
        self.window_x = app_window.x()
        self.window_y = app_window.y()
        self.window_width = app_window.frameSize().width()
        self.window_height = app_window.frameSize().height()


        # Layout
        self.v_box_main = QVBoxLayout()
        self.h_box_player_name = QHBoxLayout()
        self.h_box_options_1 = QHBoxLayout()
        self.h_box_options_2 = QHBoxLayout()

        # Labels, lineedit, buttons and other
        self.name_1_text_field = QLineEdit()
        self.name_2_text_field = QLineEdit()
        self.title_label = QLabel("Custom size TicTacToe\n by Peter Szepesi")
        self.grid_size_label = QLabel("Grid size : ")
        self.on_a_row_label = QLabel("In a row : ")
        self.grid_size_combo = QComboBox()
        self.in_a_row_combo = QComboBox()
        self.start_button = QPushButton("Start")

        self.initUI()

    def initUI(self):

        # Layout
        self.h_box_player_name.addWidget(self.name_1_text_field)
        self.h_box_player_name.addWidget(self.name_2_text_field)
        self.h_box_options_1.addWidget(self.grid_size_label)
        self.h_box_options_1.addWidget(self.grid_size_combo)
        self.h_box_options_2.addWidget(self.on_a_row_label)
        self.h_box_options_2.addWidget(self.in_a_row_combo)
        self.v_box_main.addWidget(self.title_label, alignment = Qt.AlignCenter | Qt.AlignTop)
        self.v_box_main.addLayout(self.h_box_player_name)
        self.v_box_main.addLayout(self.h_box_options_1)
        self.v_box_main.addLayout(self.h_box_options_2)
        self.v_box_main.addWidget(self.start_button, alignment = Qt.AlignCenter)
        self.setLayout(self.v_box_main)

        # Geometry
        self.center_window()

        # Event handling
        self.start_button.clicked.connect(self.start)

        # Labels, buttons and other
        self.title_label.setObjectName("titleLabel")
        self.setWindowTitle("Welcome to custom size TicTacToe")
        self.name_1_text_field.setPlaceholderText("Player 1 name : ")
        self.name_2_text_field.setPlaceholderText("Player 2 name : ")
        self.grid_size_combo.addItems(["8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        self.in_a_row_combo.addItems(["3", "4", "5", "6", "7", "8"])

        # QSS styling
        self.setStyleSheet("""
            QLabel{
                font-family: Bahnschrift;
                font-size: 25px;
            }
            
            QLabel#titleLabel{
                font-size: 35px;
                color: rgb(0, 225, 0);
                font-style: italic;
            }
            
            QComboBox{
                font-size: 15px;
            }
            
            QPushButton{
                font-family: Bahnschrift;
                font-size: 25px;
            }
            
            QLineEdit{
                font-family: Bahnschrift;
                font-size: 25px;
            }
            
            WelcomeWindow{
                background-color: rgb(220, 220, 255);
            }
        """)

    def center_window(self):
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height)

    def start(self):
        self.app_window.player_1_name = self.name_1_text_field.text()
        self.app_window.player_2_name = self.name_2_text_field.text()
        # If the name fields are empty
        if len(self.app_window.player_1_name) == 0:
            self.app_window.player_1_name = "Player 1"
        if len(self.app_window.player_2_name) == 0:
            self.app_window.player_2_name = "Player 2"
        self.app_window.grid_size = int(self.grid_size_combo.currentText())
        self.app_window.in_a_row = int(self.in_a_row_combo.currentText())

        self.app_window.player_1_label.setText(f"🟡{self.app_window.player_1_name}")
        self.app_window.player_2_label.setText(f"    {self.app_window.player_2_name}")
        self.app_window.game_info_label.setText(f"{self.app_window.in_a_row} in a row")
        self.app_window.create_buttons()
        self.hide()