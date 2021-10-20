import tkinter as tk
from tkinter import filedialog
import cv2

def Load():
    image_file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("JPG files", "*.jpg"),
                                          ("all files", "*.*")))
    print(image_file)

    img = tk.PhotoImage(file=image_file)
    label = tk.Label(win, image=img)

    # img = cv2.imread(image_file, cv2.IMREAD_COLOR)

    # cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
    # cv2.imshow('Mobile_D', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def domenu():
    print("OK")
    
win = tk.Tk()
win.geometry('300x200')
win.title("IDcard")

menubar = tk.Menu(win)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=Load)
filemenu.add_command(label="Save", command=domenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=win.quit)

win.config(menu=menubar)
win.mainloop()

