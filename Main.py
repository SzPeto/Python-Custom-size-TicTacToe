import sys

from PyQt5.QtWidgets import QApplication

from app_window import AppWindow


class Main:
    def __init__(self):
        from welcome_window import WelcomeWindow
        self.app = QApplication(sys.argv)
        self.window = AppWindow(self)
        self.window.show()
        # Welcome window
        self.welcome_w = WelcomeWindow(self.window)
        self.welcome_w.show()
        sys.exit(self.app.exec_())



if __name__ == "__main__":
    Main()
