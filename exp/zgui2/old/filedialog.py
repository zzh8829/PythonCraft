import tkinter as tk
import tkinter.filedialog as fd
import threading

rt = tk.Tk()
rt.withdraw()

def GetOpenFile():
	return fd.askopenfilename()

def GetSaveFile():
	return fd.asksaveasfilename()