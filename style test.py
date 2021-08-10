#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

s1 = 'style1.TButton'
s2 = 'style2.TButton'

s = ttk.Style()

s.map(s1, background=[('', 'red')])
s.map(s2, background=[('', 'green')])


iterator = ([s1, s2][i] for i in (0, 1))

selected_style = s1
def foo():
    global selected_style, btn

    print(selected_style)
    btn.config(style="awdark.button")
    selected_style = s1 if selected_style == s2 else s2


btn = ttk.Button(root, text='click me', command=foo)
btn.pack()

s = ttk.Style()
s.theme_names()
#root.tk.call('lappend', 'auto_path', 'E:/awthemes-10.4.0/i/awthemes')
#root.tk.call('package', 'require', 'awdark.tcl')
root.tk.call('source', 'E:/awthemes-10.4.0/awdark.tcl')
s.theme_use("awdark")
root.mainloop()