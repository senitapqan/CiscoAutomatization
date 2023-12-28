import tkinter as tk

def get_label_text():
    text = label.cget("text")
    print("Label Text:", text)

root = tk.Tk()

# Create a label
label = tk.Label(root, text="Hello, World!")
label.pack()

# Create a button to get label text
button = tk.Button(root, text="Get Label Text", command=get_label_text)
button.pack()

root.mainloop()
