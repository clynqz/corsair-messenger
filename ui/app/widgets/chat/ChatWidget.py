from .ContactsWidget import ContactsWidget
from .MessagesWidget import MessagesWidget
from .ChatWidgetQSS import ChatWidgetQSS
from .Contact import Contact
from .Message import Message
from client.Client import Client
from client.MessageReceiveThread import MessageReceiveThread
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QMainWindow

class ChatWidget(QWidget):

    def __init__(self, main_window: QMainWindow, client: Client) -> None:

        if not isinstance(main_window, QWidget):
            raise TypeError(type(main_window))
        
        if not isinstance(client, Client):
            raise TypeError(type(client))

        super().__init__()

        self.__client = client
        self.__main_window = main_window

        self.__contacts_widget = ContactsWidget(self.__search_contacts)
        self.__messages_widget = MessagesWidget(self.__client)

        self.setLayout(self.__get_main_layout())
        self.setStyleSheet(ChatWidgetQSS(main_window).qss)

        self.__load_contacts()
        
        self.__message_receive_thread = MessageReceiveThread(client)
        self.__message_receive_thread.message_received.connect(self.__message_received_slot)
        self.__message_receive_thread.start()

    def __get_main_layout(self) -> QHBoxLayout:

        layout = QHBoxLayout()

        contacts_layout = self.__get_contacts_layout()

        layout.addLayout(contacts_layout, 2)
        layout.addLayout(self.__messages_widget.layout, 5)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        return layout

    def __get_contacts_layout(self) -> QVBoxLayout:

        contacts_layout = QVBoxLayout()

        contacts_layout.addWidget(self.__contacts_widget.contacts_search)
        contacts_layout.addWidget(self.__contacts_widget.contacts_scrollarea)

        return contacts_layout
    
    def __load_contacts(self) -> None:

        contacts = self.__client.get_contacts()

        for raw_contact in contacts:

            contact_id = int(raw_contact["user_id"])
            nickname = raw_contact["nickname"]

            contact = Contact(
                contact_id, 
                nickname,
                self.__contact_selected_callback, 
                self.__message_sent_callback, 
                self.__client.pull_messages, 
                self.__main_window
                )

            self.__contacts_widget.add_contact(contact)

    def __search_contacts(self, pattern: str) -> None:

        contacts = self.__client.search_contacts(pattern)

        for raw_contact in contacts:

            contact_id = int(raw_contact["user_id"])
            nickname = raw_contact["nickname"]

            contact = Contact(
                contact_id, 
                nickname, 
                self.__contact_selected_callback, 
                self.__message_sent_callback, 
                self.__client.pull_messages, 
                self.__main_window
                )

            self.__contacts_widget.add_contact(contact)

    def __contact_selected_callback(self, contact: Contact) -> None:

        if not isinstance(contact, Contact):
            raise TypeError(type(contact))
        
        self.__messages_widget.hide_contact_dialog()
        self.__messages_widget.show_contact_dialog(contact)

        previous_contact = self.__messages_widget.contact
        self.__messages_widget.contact = contact

        if previous_contact is None:
            return

        previous_contact.setObjectName("") 
        previous_contact.setStyleSheet("") 

    def __message_sent_callback(self, receiver_id: int, text: str) -> None:
        
        if not isinstance(receiver_id, int):
            raise TypeError(type(receiver_id))
        
        if not isinstance(text, str):
            raise TypeError(type(text))

        self.__client.send_message(receiver_id=receiver_id, text=text)

    def __message_received_slot(self, raw_message: dict) -> None:

        message_type = int(raw_message["type"])

        if message_type == 0:
            self.__receive_new_message(raw_message)
        elif message_type == 1:
            self.__receive_delivery_callback_message(raw_message)
        else:
            raise ValueError(message_type)

    def __receive_delivery_callback_message(self, raw_message: dict) -> None:

        user_id = int(raw_message["user_id"])
        text = raw_message["text"]
        send_time = raw_message["send_time"] # todo

        message = Message(text)

        self.__contacts_widget.contacts[user_id].add_message(message, True)

    def __receive_new_message(self, raw_message: dict) -> None:

        sender_id = int(raw_message["sender_id"])
        text = raw_message["text"]
        send_time = raw_message["send_time"] # todo        

        message = Message(text)

        self.__contacts_widget.contacts[sender_id].add_message(message, False)
