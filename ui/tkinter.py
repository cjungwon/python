import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu

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

chVarDis = tk.IntVar()
check1 = tk.Checkbutton(win, text='Disabled', variable=chVarDis, state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W)

chVarUn = tk.IntVar()
check2= tk.Checkbutton(win, text='UnChecked', variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(win, text='Enabled', variable=chVarEn)
check3.select()
check3.grid(column=2, row=4, sticky=tk.W)

colors = ['Blue', 'Gold', 'Red']

def radCall():
    radSel=radVar.get()
    if radSel == 0: win.configure(background=colors[0])
    elif radSel == 1: win.configure(background=colors[1])
    elif radSel == 2: win.configure(background=colors[2])

radVar = tk.IntVar()

radVar.set(99)

for col in range(3):
    curRad = tk.Radiobutton(win, text=colors[col], variable=radVar, value=col, command=radCall)
    curRad.grid(column=col, row=5, sticky=tk.W)

scrol_w = 30
scrol_h = 3
scr = scrolledtext.ScrolledText(win, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scr.grid(column=0, columnspan=3)

menu_bar = Menu(win)
win.config(menu=menu_bar)

file_menu = Menu(menu_bar)
file_menu.add_command(label='New')
file_menu.add_command(label='Exit')
menu_bar.add_cascade(label='File', menu=file_menu)

name_entered.focus()

win.mainloop()