import tkinter
import threading
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
        self.username = self.username_entry.get()
        self.client_socket = client.Client(self.username)
        
        self.t = threading.Thread(target = self.receive)
        self.t.start()

        self.username_entry.unbind('<Return>')
        self.init_main_window()

    def init_main_window(self):
        messages_frame = tkinter.Frame(self.master)
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list = tkinter.Listbox(messages_frame, height=34, width=62, yscrollcommand=scrollbar.set)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()

        messages_frame.pack()

        self.message_entry = tkinter.Entry(self.master, width = 65)
        self.message_entry.bind("<Return>", self.send)
        self.message_entry.pack()
        send_button = tkinter.Button(self.master, text="Send", command = self.send, width = 65, height = 2)
        send_button.pack()

    def send(self, event = None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tkinter.END)
        if len(message) > 0:
            self.msg_list.insert(tkinter.END, self.username + ': ' + message)
        try:
            self.client_socket.send_message(message)
        except ConnectionResetError:
            print('Connection error')
            self.master.destroy()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recieve_message()
                self.msg_list.insert(tkinter.END, message)
            except OSError:
                print('Server aborted connection')
                self.master.destroy()

    def on_closing(self):
        self.client_socket.send_message('Leaving...server')
        self.master.destroy()

def main():
    root = tkinter.Tk()
    root.title("Chat app")
    root.geometry('400x600')

    window = ChatWindow(root)
    root.protocol("WM_DELETE_WINDOW", window.on_closing)

    tkinter.mainloop()  # Starts GUI execution

if __name__ == '__main__':
    main()
