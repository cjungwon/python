import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

global id_pw_list
id_pw_list = {'id' : '', 'pw' : ''}
id_pw_list['id'] = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff' ,'ggg', 'hhh', 'iii', 'jjj']
id_pw_list['pw'] = ['111', '222', '333', '444', '555', '666' ,'777', '888', '999', '000']

win = tk.Tk()

win.geometry('250x250')
win.title("LogIn")

ttk.Label(win, text='ID : ').grid(column=0, row=0)
ttk.Label(win, text='Password : ').grid(column=0, row=1)

id = tk.StringVar()
id_entered = ttk.Entry(win, width=15, textvariable=id)
id_entered.grid(column=1, row=0)

pw = tk.StringVar()
pw_entered = ttk.Entry(win, width=15, textvariable=pw)
pw_entered.grid(column=1, row=1)


def login():
    if id.get() in id_pw_list['id']:

        if id_pw_list['id'].index(id.get()) == id_pw_list['pw'].index(pw.get()):
            msg.showinfo("로그인", "로그인 완료")
        else:
            msg.showerror("로그인 실패", "Password가 일치하지 않음")
            
    else:
        msg.showerror("로그인 실패", "ID를 찾을 수 없음")

def reset():
    id_entered.delete(0, "end")
    pw_entered.delete(0, "end")

    

bnt_login = ttk.Button(win, text="Login", command=login)
bnt_login.grid(column=0, row=2)

bnt_reset = ttk.Button(win, text="Reset", command=reset)
bnt_reset.grid(column=1, row=2)

win.mainloop()