__author__ = 'Tom'

from tkinter import *
from tkinter.ttk import *

COLORS = ["white", "black", "red", "orange", "yellow", "green", "blue", "purple"]
FONTS = ["Arial", "Courier New", "Comic Sans MS", "Fixedsys", "MS Sans Serif",
         "MS Serif", "Symbol", "System", "Times New Roman", "Verdana"]

class Message:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrolling Message")
        self.root.resizable(0, 0)
        self.canvas = Canvas(self.root, width=500, height=500)
        self.canvas.pack(fill='both', expand='yes')
        self.top_level = None
        self.label = StringVar()
        self.font = StringVar()
        self.font.set(FONTS[0])
        self.foreground = StringVar()
        self.foreground.set(COLORS[0])
        self.background = StringVar()
        self.background.set(COLORS[0])
        self.speed = None
        self.message_speed = 0
        self.direction = StringVar()
        self.direction.set("Left")
        self.message = None
        self.after = None
        self.add_menu()

    def add_menu(self):
        menu = Menu(self.root)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New Message", command=self.new_message)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

    def new_message(self):
        if self.top_level is not None and self.top_level.winfo_exists():
            self.top_level.focus()
        else:
            self.top_level = Toplevel(self.root, padx=10, pady=10)
            self.top_level.title("New Message")
        Label(self.top_level, text="Label").grid(row=0, column=0)
        Entry(self.top_level, textvariable=self.label).grid(row=0, column=1, sticky="w")
        Label(self.top_level, text="Font").grid(row=1, column=0)
        OptionMenu(self.top_level, self.font, "", *FONTS).grid(row=1, column=1, sticky="w")
        Label(self.top_level, text="Foreground").grid(row=2, column=0)
        OptionMenu(self.top_level, self.foreground, "", *COLORS).grid(row=2, column=1, sticky="w")
        Label(self.top_level, text="Background").grid(row=3, column=0)
        OptionMenu(self.top_level, self.background, "", *COLORS).grid(row=3, column=1, sticky="w")
        Label(self.top_level, text="Speed").grid(row=4, column=0)
        self.speed = Scale(self.top_level, from_=1, to=5000)
        self.speed.set(self.message_speed)
        self.speed.grid(row=4, column=1, sticky="w")
        Label(self.top_level, text="Direction").grid(row=5, column=0)
        OptionMenu(self.top_level, self.direction, "", "Left", "Right").grid(row=5, column=1, sticky="w")
        Button(self.top_level, text="Add", command=self.add_message).grid(row=6, column=1, pady=10, sticky="w")

    def add_message(self):
        if self.message is None:
            self.message = self.canvas.create_text(self.canvas.winfo_width() // 2,
                                                   (self.canvas.winfo_height() // 2) - 25)
        self.canvas.itemconfigure(self.message, text=self.label.get(), font=(self.font.get(), 20),
                                  fill=self.foreground.get())
        self.canvas.configure(bg=self.background.get())
        self.message_speed = int(self.speed.get())
        self.message_direction = -1 if self.direction.get() == "Left" else 1
        if self.after is not None:
            self.canvas.after_cancel(self.after)
        self.move_message()
        self.top_level.destroy()

    def move_message(self):
        if self.message_direction < 0:
            if self.canvas.bbox(self.message)[2] < 0:
                self.canvas.coords(self.message, self.canvas.winfo_width() + (self.get_message_width() // 2),
                                   (self.canvas.winfo_height() // 2) - 25)
        else:
            if self.canvas.bbox(self.message)[0] > self.canvas.winfo_width():
                self.canvas.coords(self.message, -(self.get_message_width() // 2), (self.canvas.winfo_height() // 2) - 25)
        self.canvas.move(self.message, self.message_direction, 0)
        self.after = self.canvas.after(5000 - self.message_speed + 1, self.move_message)

    def get_message_width(self):
        return (self.canvas.bbox(self.message)[2] - self.canvas.bbox(self.message)[0])

if __name__ == "__main__":
    root = Tk()
    message = Message(root)
    root.mainloop()