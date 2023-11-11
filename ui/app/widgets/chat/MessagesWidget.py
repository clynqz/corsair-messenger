from .MessageEdit import MessageEdit
from .Scrollarea import Scrollarea
from .Message import Message
from PyQt6 import QtCore
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QLabel, QMainWindow

class MessagesWidget(QWidget):

    def __init__(self, main_window: QMainWindow, parent: QWidget) -> None:

        if not isinstance(main_window, QMainWindow):
            raise TypeError(type(main_window))
        
        if not isinstance(parent, QWidget):
            raise TypeError(type(parent))
        
        super().__init__(parent)

        self.__current_contact_name = QLabel("clynqz")
        self.__messages_scrollarea = Scrollarea(self, self.__messages_scrollarea_enter_event, self.__messages_scrollarea_leave_event)
        self.__message_edit = self.__get_message_edit(main_window)

        self.__messages_scrollarea.layout.addStretch(1)

        self.__current_contact_name.setObjectName("currentContactName")
        self.__messages_scrollarea.verticalScrollBar().setObjectName("showed")

    @property
    def current_contact_name(self) -> QLabel:
        return self.__current_contact_name
    
    @property
    def messages_scrollarea(self) -> Scrollarea:
        return self.__messages_scrollarea
    
    @property
    def message_edit(self) -> QTextEdit:
        return self.__message_edit

    def add_message(self, message: Message, self_author: bool) -> None:

        if not isinstance(message, Message):
            raise TypeError(type(message)) 
        
        if not isinstance(self_author, bool):
            raise TypeError(type(self_author)) 

        message_layout = QVBoxLayout()

        alignment = (QtCore.Qt.AlignmentFlag.AlignRight if self_author else QtCore.Qt.AlignmentFlag.AlignLeft) | QtCore.Qt.AlignmentFlag.AlignBottom

        message_layout.addWidget(message)
        message_layout.setAlignment(alignment)

        self.__messages_scrollarea.layout.addLayout(message_layout)   

        message_layout.update()

    def __get_message_edit(self, main_window: QMainWindow) -> QTextEdit:

        if not isinstance(main_window, QMainWindow):
            raise TypeError(type(main_window))
        
        message_edit_max_height = main_window.size().height() // 3
        
        message_edit = MessageEdit(self, message_edit_max_height)

        message_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        message_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        message_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        return message_edit
    
    def __messages_scrollarea_enter_event(self) -> None:

        scrollarea = self.__messages_scrollarea
        scrollbar = scrollarea.verticalScrollBar()

        if scrollbar.maximum() != 0:
            scrollbar.show()

    def __messages_scrollarea_leave_event(self) -> None:

        scrollarea = self.__messages_scrollarea
        scrollbar = scrollarea.verticalScrollBar()

        if not scrollbar.isHidden():
            scrollbar.hide()
