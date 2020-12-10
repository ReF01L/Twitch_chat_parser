import socket
import config
import logging
from tkinter import *
from tkinter import simpledialog, messagebox
import threading


class Main(Frame):
    class MyThread(threading.Thread):
        def __init__(self, sock=None):
            threading.Thread.__init__(self)
            self.sock = sock
            self.is_start = False

        def run(self):
            self.is_start = True
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s — %(message)s',
                datefmt='%Y-%m-%d_%H:%M:%S',
                handlers=[logging.FileHandler('chat.log', encoding='utf-8')]
            )

            while self.is_start:
                resp = self.sock.recv(2048).decode('utf-8')

                if len(resp) > 0:
                    logging.info(resp)

            self.sock.close()

        def stop(self):
            self.is_start = False

    def __init__(self, _root):
        super(Main, self).__init__(_root)
        self.build()
        self.is_start = False

    def build(self):
        self.lbl = Label(text=f'Current channel: ', font=('Times New Roman', 21, 'bold'),
                         bg='#FFF',
                         foreground='#000')
        self.lbl.place(x=80, y=50)

        self.channel_lbl = Label(text=config.CHAN, font=('Times New Roman', 23, 'italic'),
                                 bg='#FFF',
                                 foreground='#000')
        self.channel_lbl.place(x=80, y=100)

        start_btn = Button(text='Start parse', bg='#FFF', font=('Times New Roman', 15),
                           command=lambda: self.start()).place(
            x=180,
            y=150,
        )
        change_chan_btn = Button(text='Change channel', bg='#FFF', font=('Times New Roman', 15),
                                 command=lambda: self.change_chan()).place(
            x=160,
            y=200
        )
        self.stop_btn = Button(text='Stop', command=lambda: self.stop(), state=DISABLED)
        self.stop_btn.place(x=180, y=250, width=100)

    def stop(self):
        self.thread.stop()
        self.is_start = False
        self.thread.join()
        self.stop_btn.configure(state=DISABLED)

    def start(self):
        self.is_start = True
        self.stop_btn.configure(state=NORMAL)

        sock = socket.socket()
        sock.connect((config.HOST, config.PORT))

        sock.send(f"PASS {config.PASS}\n".encode('utf-8'))
        sock.send(f"NICK {config.NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {config.CHAN}\n".encode('utf-8'))

        self.thread = self.MyThread(sock)
        self.thread.start()

    def change_chan(self):
        if self.is_start:
            stop = messagebox.askyesno('The program is running', 'Stop the program?')
            if stop:
                self.stop()
            else:
                return

        answer = simpledialog.askstring("Change channel", "What channel do you want to follow?", parent=root)
        if not answer:
            messagebox.showwarning('Attention!', 'You haven\'t changed the name of the channel.')
        else:
            config.CHAN = '#' + answer
            self.channel_lbl.configure(text=config.CHAN)
            config.swap_channel(config.CHAN)


if __name__ == '__main__':
    root = Tk()
    root['bg'] = "#FFF"
    root.geometry("500x500")
    root.title("Twitch chat parser")
    root.resizable(FALSE, FALSE)
    app = Main(root)
    app.pack()
    root.mainloop()
