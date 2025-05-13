import sys

from PyQt5.QtWidgets import QApplication

from app_window import AppWindow


def main():
    from welcome_window import WelcomeWindow
    welcome_w: WelcomeWindow
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    # Welcome window
    welcome_w = WelcomeWindow(window)
    welcome_w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
