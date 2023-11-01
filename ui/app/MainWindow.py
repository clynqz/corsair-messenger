from .widgets.login.LoginWidget import LoginWidget
from .MainWindowQSS import MainWindowQSS
from .widgets.login.LoginWidgetQSS import LoginWidgetQSS
from .widgets.chat.ChatWidget import ChatWidget
from helpers.QSSHelper import QSSHelper
from PyQt6 import QtGui
from os.path import (
    dirname, realpath,
)
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QApplication,
)

#self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        
        super().__init__()

        self.__screen_size = QApplication.primaryScreen().size()

        self.__set_window_geometry()
        
        self.__font_id = MainWindow.__add_app_font()

        central_widget = ChatWidget(self)
        #central_widget = LoginWidget(self)

        self.setCentralWidget(central_widget)
        
        self.setStyleSheet(MainWindowQSS().qss)

    @staticmethod
    def __add_app_font() -> int:

        font_path = rf"{dirname(realpath(__file__))}\appFont.ttf"
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)

        return font_id

    def __set_window_geometry(self) -> None:

        self.setFixedWidth(int(self.__screen_size.width() / 1.5))
        self.setFixedHeight(int(self.__screen_size.height() / 1.5))
