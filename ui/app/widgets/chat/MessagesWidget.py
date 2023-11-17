from .Contact import Contact
from client.Client import Client
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MessagesWidget(QWidget):

    def __init__(self, client: Client) -> None:

        if not isinstance(client, Client):
            raise TypeError(type(client))

        super().__init__()

        self.__contact = None
        self.__client = client

        self.__layout = self.__get_messages_layout()

    @property
    def layout(self) -> QVBoxLayout:
        return self.__layout

    @property
    def contact(self) -> Contact:
        return self.__contact
    
    @contact.setter
    def contact(self, contact: Contact) -> Contact:

        if not isinstance(contact, Contact):
            raise TypeError(type(contact))

        self.__contact = contact

    def hide_contact_dialog(self) -> None:

        for i in range(self.__layout.count()): 
            self.__layout.itemAt(0).widget().setParent(None)

    def show_contact_dialog(self, contact: Contact) -> None:

        if not isinstance(contact, Contact):
            raise TypeError(type(contact))

        currentContactName = QLabel(contact.text())

        currentContactName.setObjectName("currentContactName")

        self.__layout.addWidget(currentContactName)
        self.__layout.addWidget(contact.messages_scrollarea)
        self.__layout.addWidget(contact.message_edit)

    def __get_messages_layout(self) -> QVBoxLayout:

        messages_layout = QVBoxLayout()

        return messages_layout
    