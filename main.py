import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("MyApp")
    root.geometry("360x140")

    ttk.Label(root, text="Hello from a tiny executable 👋").pack(pady=18)
    ttk.Button(root, text="Quit", command=root.destroy).pack()

    root.mainloop()

if __name__ == "__main__":
    main()