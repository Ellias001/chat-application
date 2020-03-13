import tkinter
import client

class ChatWindow:
    def __init__(self, master):
        self.master = master
        self.init_hello_window()
    
    def init_hello_window(self):
        label = tkinter.Label(self.master, text = 'Username', font = ('bold', 12))
        label.place(x = 150, y = 200)
        
        self.username_entry = tkinter.Entry(self.master)
        self.username_entry.place(x = 125, y = 220)

        self.username_entry.bind('<Return>', self.init_client_socket)

    def init_client_socket(self, event):
        username = self.username_entry.get()
        self.client_socket = client.Client(username)
        self.username_entry.unbind('<Return>')
        self.init_main_window()

    def init_main_window(self):
        messages_frame = tkinter.Frame(self.master)
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        msg_list.pack()

        messages_frame.pack()

        self.message_entry = tkinter.Entry(self.master)
        self.message_entry.bind("<Return>", self.send)
        self.message_entry.pack()
        send_button = tkinter.Button(self.master, text="Send", command = self.send)
        send_button.pack()

    def send(self, event = None):
        message = self.message_entry.get()
        self.client_socket.send_message(message)
                
def main():
    root = tkinter.Tk()
    root.title("Chat app")
    root.geometry('400x600')

    window = ChatWindow(root)

    tkinter.mainloop()  # Starts GUI execution.

if __name__ == '__main__':
    main()
