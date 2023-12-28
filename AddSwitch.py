import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
from api import Switch


class AddSwitchDialog(tk.Toplevel):
    def __init__(self, parent, listbox, apiObjects):
        super().__init__(parent)
        self.title("Add Switch")
        self.listbox = listbox
        self.apiObjects = apiObjects

        self.switch_host_label = ttk.Label(self, text="Host:")
        self.switch_host_label.grid(row=0, column=0, padx=10, pady=10)

        self.switch_host_entry = ttk.Entry(self)
        self.switch_host_entry.grid(row=0, column=1, padx=10, pady=10)

        self.switch_username_label = ttk.Label(self, text="Username:")
        self.switch_username_label.grid(row=1, column=0, padx=10, pady=10)

        self.switch_username_entry = ttk.Entry(self)
        self.switch_username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.switch_password_label = ttk.Label(self, text="Password:")
        self.switch_password_label.grid(row=2, column=0, padx=10, pady=10)

        self.switch_password_entry = ttk.Entry(self)
        self.switch_password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.switch_epassword_label = ttk.Label(self, text="Enable Pass:")
        self.switch_epassword_label.grid(row=3, column=0, padx=10, pady=10)

        self.switch_epassword_entry = ttk.Entry(self)
        self.switch_epassword_entry.grid(row=3, column=1, padx=10, pady=10)

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect_switch)
        self.connect_button.grid(row=4, column=1, pady=10)

    def connect_switch(self):
        switch_host = self.switch_host_entry.get()
        switch_username = self.switch_username_entry.get()
        switch_password = self.switch_password_entry.get()
        switch_epassword = self.switch_epassword_entry.get()
        switch = Switch()

        if switch_host:
            host = switch.connect_to_switch(switch_host, switch_username, switch_password, switch_epassword)
            if host:
                self.listbox.insert(tk.END, host[0])
                self.apiObjects.append(host[1])
        self.destroy()

