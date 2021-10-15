import tkinter as tk
from tkinter import ttk
from tkinter.constants import NUMERIC

win = tk.Tk()

win.title("Python GUI")

def click_me():
    action.configure(text="Hello " + name.get() + ' ' + number_chosen.get())

action = ttk.Button(win, text='Click Me!', command=click_me)
action.grid(column=2, row=1)

ttk.Label(win, text='Enter a name: ').grid(column=0, row=0)
ttk.Label(win, text='Choose a number: ').grid(column=1, row=0)

name = tk.StringVar()
name_entered = ttk.Entry(win, width=12, textvariable=name)
name_entered.grid(column=0, row=1)

number = tk.StringVar()
number_chosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=1)
number_chosen.current(0)

name_entered.focus()

win.mainloop()

# p.27