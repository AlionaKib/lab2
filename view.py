# -*- coding: utf-8 -*-
import tkinter
import messages

from tkinter import messagebox, simpledialog


CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"
COLORS_CODE_DICTIONARY = {0: '#FFFF00',
                          1: '#00FFFF',
                          2: '#00FF00',
                          3: '#FF00FF',
                          4: '#FF0000'}
COLORS_NAME_DICTIONARY = {0: 'y',
                          1: 'b',
                          2: 'g',
                          3: 'p',
                          4: 'r'}


class EzChatUI(object):

    def __init__(self, application):
        self.application = application
        self.gui = None
        self.frame = None
        self.input_field = None
        self.message = None
        self.message_list = None
        self.scrollbar = None
        self.send_button = None
        self.start_label = None
        self.turn_label = None

        self.button_blue = None
        self.button_yellow = None
        self.button_green = None
        self.button_pink = None
        self.button_red = None

        self.label1 = None
        self.label2 = None
        self.label3 = None
        self.label4 = None
        self.label5 = None
        self.colors_buttons_label = None
        self.colors_label = None
        self.timer = None

        self.colors_frame = None
        self.colors_labels_frame = None

        self.current_label = 0
        self.current_color = 0
        self.colors_sequence = list('yyyyy')

    def show(self):
        self.gui = tkinter.Tk()
        self.gui.title(messages.TITLE)
        self.fill_frame()
        self.gui.protocol(CLOSING_PROTOCOL, self.on_closing)
        return self.input_dialogs()

    def loop(self):
        self.gui.mainloop()

    def yellow_click(self):
        self.current_color = 0
        self.color_click()

    def blue_click(self):
        self.current_color = 1
        self.color_click()

    def green_click(self):
        self.current_color = 2
        self.color_click()

    def pink_click(self):
        self.current_color = 3
        self.color_click()

    def red_click(self):
        self.current_color = 4
        self.color_click()

    def color_click(self):
        if self.current_label == 1:
            self.label2.config(bg=COLORS_CODE_DICTIONARY.get(self.current_color), relief=tkinter.GROOVE)
            self.label3.config(relief=tkinter.SUNKEN)
        elif self.current_label == 2:
            self.label3.config(bg=COLORS_CODE_DICTIONARY.get(self.current_color), relief=tkinter.GROOVE)
            self.label4.config(relief=tkinter.SUNKEN)
        elif self.current_label == 3:
            self.label4.config(bg=COLORS_CODE_DICTIONARY.get(self.current_color), relief=tkinter.GROOVE)
            self.label5.config(relief=tkinter.SUNKEN)
        elif self.current_label == 4:
            self.label5.config(bg=COLORS_CODE_DICTIONARY.get(self.current_color), relief=tkinter.GROOVE)
            self.label1.config(relief=tkinter.SUNKEN)
        else:
            self.current_label = 0
            self.label1.config(bg=COLORS_CODE_DICTIONARY.get(self.current_color), relief=tkinter.GROOVE)
            self.label2.config(relief=tkinter.SUNKEN)

        self.colors_sequence[self.current_label] = COLORS_NAME_DICTIONARY.get(self.current_color)
        self.current_label = self.current_label + 1

        temp = ''
        for i in self.colors_sequence:
            temp = temp + i + ' '
        new_text = "Your sequence: " + temp
        self.colors_label.config(text=new_text)
        self.message.set(temp)

    def click_send(self):
        if self.current_label == 1:
            self.label2.config(relief=tkinter.GROOVE)
        if self.current_label == 2:
            self.label3.config(relief=tkinter.GROOVE)
        if self.current_label == 3:
            self.label4.config(relief=tkinter.GROOVE)
        if self.current_label == 4:
            self.label5.config(relief=tkinter.GROOVE)
        self.current_label = 0
        self.label1.config(relief=tkinter.SUNKEN)
        self.disable_send_button()
        self.application.send()

    def fill_frame(self):
        self.frame = tkinter.Frame(self.gui)
        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame, state=TEXT_STATE_DISABLED)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message = tkinter.StringVar()
        self.message.set("y y y y y ")
        self.frame.pack()

        self.colors_frame = tkinter.Frame(self.gui)
        self.colors_frame.pack()
        self.colors_buttons_label = tkinter.Label(self.colors_frame, text='Input color sequence')
        self.button_yellow = tkinter.Button(self.colors_frame, bg='#FFFF00', width=8, height=2, text='yellow',
                                          command=self.yellow_click)
        self.button_blue = tkinter.Button(self.colors_frame, bg='#00FFFF', width=8, height=2, text='blue',
                                            command=self.blue_click)
        self.button_green = tkinter.Button(self.colors_frame, bg='#00FF00', width=8, height=2, text='green',
                                            command=self.green_click)
        self.button_pink = tkinter.Button(self.colors_frame, bg='#FF00FF', width=8, height=2, text='pink',
                                            command=self.pink_click)
        self.button_red = tkinter.Button(self.colors_frame, bg='#FF0000', width=8, height=2, text='red',
                                            command=self.red_click)
        self.colors_buttons_label.pack(side=tkinter.TOP)
        self.button_yellow.pack(side=tkinter.LEFT)
        self.button_blue.pack(side=tkinter.LEFT)
        self.button_green.pack(side=tkinter.LEFT)
        self.button_pink.pack(side=tkinter.LEFT)
        self.button_red.pack(side=tkinter.LEFT)

        self.colors_labels_frame = tkinter.Frame(self.gui)
        self.colors_labels_frame.pack()
        self.colors_label = tkinter.Label(self.colors_labels_frame, text='Your sequence: y y y y y ')
        self.label1 = tkinter.Label(self.colors_labels_frame, width=8, height=2, bg='#FFFF00', relief=tkinter.SUNKEN)
        self.label2 = tkinter.Label(self.colors_labels_frame, width=8, height=2, bg='#FFFF00', relief=tkinter.GROOVE)
        self.label3 = tkinter.Label(self.colors_labels_frame, width=8, height=2, bg='#FFFF00', relief=tkinter.GROOVE)
        self.label4 = tkinter.Label(self.colors_labels_frame, width=8, height=2, bg='#FFFF00', relief=tkinter.GROOVE)
        self.label5 = tkinter.Label(self.colors_labels_frame, width=8, height=2, bg='#FFFF00', relief=tkinter.GROOVE)
        self.colors_label.pack(side=tkinter.TOP)
        self.label1.pack(side=tkinter.LEFT)
        self.label2.pack(side=tkinter.LEFT)
        self.label3.pack(side=tkinter.LEFT)
        self.label4.pack(side=tkinter.LEFT)
        self.label5.pack(side=tkinter.LEFT)

        self.send_button = tkinter.Button(self.gui, text=messages.SEND, command=self.click_send, state=tkinter.DISABLED)
        self.send_button.pack()

        self.timer = tkinter.Label(self.gui, font="Arial 23", width=10, height=3, fg='#FF0000')
        self.timer.pack(side=tkinter.RIGHT)

        self.start_label = tkinter.Label(self.gui, text="You can pick now or wait")
        self.turn_label = tkinter.Label(self.gui, text="Now your turn")

    def input_dialogs(self):
        self.gui.lower()
        username = simpledialog.askstring(messages.USERNAME, messages.INPUT_USERNAME, parent=self.gui)
        self.gui.title("COLOR GAME. Player " + username)
        self.application.username = username
        if self.application.username is None:
            return False
        self.application.host = simpledialog.askstring(messages.SERVER_HOST, messages.INPUT_SERVER_HOST,
                parent=self.gui)
        if self.application.host is None:
            return False
        self.application.port = simpledialog.askinteger(messages.SERVER_PORT, messages.INPUT_SERVER_PORT,
                parent=self.gui)
        if self.application.port is None:
            return False
        return True

    def alert(self, title, message):
        messagebox.showerror(title, message)

    def show_send_button(self):
        self.send_button.config(state=tkinter.ACTIVE)

    def disable_send_button(self):
        self.send_button.config(state=tkinter.DISABLED)

    def show_timer(self, message):
        self.timer.config(text=message.message)

    def show_message(self, message):
        self.timer.config(text='')
        self.message_list.configure(state=TEXT_STATE_NORMAL)
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)
        self.message_list.configure(state=TEXT_STATE_DISABLED)

    def on_closing(self):
        self.application.exit()
        self.gui.destroy()


