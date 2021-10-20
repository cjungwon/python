import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

_id_pw_list = {'id' : '', 'pw' : ''}
_id_pw_list['id'] = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff' ,'ggg', 'hhh', 'iii', 'jjj']
_id_pw_list['pw'] = ['111', '222', '333', '444', '555', '666' ,'777', '888', '999', '000']

class Login:

    def __init__(self) -> None:
        pass
        
    def login(self):
        if id.get() in _id_pw_list['id']:

            if pw.get() in _id_pw_list['pw']:
                if _id_pw_list['id'].index(id.get()) == _id_pw_list['pw'].index(pw.get()):
                    msg.showinfo("로그인 완료", "로그인 되었습니다.")
                else:
                    msg.showerror("로그인 실패", "Password가 일치하지 않음")
            else:
                msg.showerror("로그인 실패", "Password가 일치하지 않음")
                
        else:
            msg.showerror("로그인 실패", "ID를 찾을 수 없음")

    def reset(self):
        edit_id.delete(0, "end")
        edit_pw.delete(0, "end")

    def show_list(self):
        win_lst = tk.Tk()
        win_lst.geometry('450x250')
        win_lst.title("ID-Password list")
        
        ttk.Label(win_lst, text='ID').grid(column=0, row=0, padx=20, pady=20)
        ttk.Label(win_lst, text='Password').grid(column=2, row=0)

        listbox_id = tk.Listbox(win_lst, selectmode="browse", height=0)
        for item in _id_pw_list['id']:
            listbox_id.insert(tk.END, item)
        listbox_id.grid(column=0, row=1, padx=20)

        listbox_pw = tk.Listbox(win_lst, selectmode="browse", height=0)
        for item in _id_pw_list['pw']:
            listbox_pw.insert(tk.END, item)
        listbox_pw.grid(column=2, row=1, padx=20)

        def match():
            listbox_pw.selection_set(listbox_id.curselection()[0])
            
        btn_match = ttk.Button(win_lst, text="->", width=5, command=match)
        btn_match.grid(column=1, row=1)

log = Login()


win = tk.Tk()
win.geometry('300x200')
win.title("LogIn")

ttk.Label(win, text='ID : ').grid(column=0, row=0, padx=40, pady=20)
ttk.Label(win, text='Password : ').grid(column=0, row=1)


id = tk.StringVar()
edit_id = ttk.Entry(win, width=15, textvariable=id)
edit_id.grid(column=1, row=0)

pw = tk.StringVar()
edit_pw = ttk.Entry(win, width=15, textvariable=pw)
edit_pw.grid(column=1, row=1)


btn_login = ttk.Button(win, text="Login", command=log.login)
btn_login.grid(column=0, row=2, padx=20, pady=20)

btn_reset = ttk.Button(win, text="Reset", command=log.reset)
btn_reset.grid(column=1, row=2, padx=20, pady=20)

btn_list = ttk.Button(win, text="List", command=log.show_list)
btn_list.grid(column=1, row=3)


win.mainloop()