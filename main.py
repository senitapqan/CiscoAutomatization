import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, filedialog

import pandas as pd

from AddSwitch import *
from api import Switch


class NetworkTester:
    def __init__(self, root):
        self.root = root
        root.title("Network Tester")
        root.geometry("1080x700")
        root.resizable(False, False)

        self.category_var = tk.StringVar()
        self.category_var.set("")

        self.current_info = list()
        self.switches = list()

        self.draw_gui()

    def draw_gui(self):
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 12))

        self.category_buttons_frame = ttk.Frame(self.root)
        self.category_buttons_frame.pack(pady=10)

        self.icp_button = ttk.Button(self.category_buttons_frame, text="IP Config",
                                     command=lambda: self.set_category("IP"), style="TButton")
        self.icp_button.grid(row=0, column=0, padx=10)

        self.routing_button = ttk.Button(self.category_buttons_frame, text="Routing",
                                         command=lambda: self.set_category("Routing"), style="TButton")
        self.routing_button.grid(row=0, column=1, padx=10)

        self.vlan_button = ttk.Button(self.category_buttons_frame, text="VLAN",
                                      command=lambda: self.set_category("VLAN"), style="TButton")
        self.vlan_button.grid(row=0, column=2, padx=10)

        device_frame = ttk.Frame(self.root)
        device_frame.pack(pady=10, padx=(0.05 * self.root.winfo_screenwidth(), 0.05 * self.root.winfo_screenwidth()),
                          fill=tk.BOTH, expand=True, side=tk.TOP)

        self.device_listbox = tk.Listbox(device_frame, selectmode=tk.MULTIPLE, height=10, width=40, bg="#f0f0f0")
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.device_listbox_scrollbar = ttk.Scrollbar(device_frame, orient="vertical",
                                                      command=self.device_listbox.yview)
        self.device_listbox.config(yscrollcommand=self.device_listbox_scrollbar.set)
        self.device_listbox_scrollbar.pack(side="right", fill="y")

        self.add_switch_button = tk.Button(self.root, text="Add Switch", command=self.add_switch, bg='#2196F3',
                                           fg='white')
        self.add_switch_button.pack(pady=10, padx=10, side=tk.TOP)

        self.show_button = tk.Button(self.root, text="Show", command=self.show_info, bg='#2196F3', fg='white')
        self.show_button.pack(pady=10, padx=10, side=tk.TOP)

        self.info_text = scrolledtext.ScrolledText(self.root, height=15, width=70, bg="#f0f0f0")
        self.info_text.pack(pady=10, padx=(0.05 * self.root.winfo_screenwidth(), 0.05 * self.root.winfo_screenwidth()),
                            fill=tk.BOTH, expand=True, side=tk.TOP)

        self.spec_frame = tk.Frame(self.root)
        self.spec_frame.pack(pady=10, side=tk.TOP)

        self.check_button = tk.Button(self.spec_frame, text = "Check", command=self.check_info, bg='#2196F3', fg='white')
        self.check_button.pack(pady=10, padx = 10, side=tk.LEFT, anchor=tk.CENTER)

        self.save_button = tk.Button(self.spec_frame, text="Save", command=self.save_info, bg='#4CAF50', fg='white')
        self.save_button.pack(pady=10, padx=10, side=tk.LEFT, anchor=tk.CENTER)

        self.answers_button = tk.Button(self.spec_frame, text="Upload answers", command=self.upload_answers, bg='#4CAF50', fg='white')
        self.answers_button.pack(pady=10, padx=10, side=tk.LEFT, anchor=tk.CENTER)

        self.file_label = tk.Label(self.spec_frame, text="None")
        self.file_label.pack(pady=10)

    def set_category(self, category):
        self.category_var.set(category)

    def add_switch(self):
        add_switch_dialog = AddSwitchDialog(self.root, self.device_listbox, self.switches)
        self.root.wait_window(add_switch_dialog)

    def listToString(self, lst):
        result = ""
        for dct in lst:
            for key in dct.keys():
                result += f"{key} : {dct[key]} "
            result += "\n"

        return result + "\n"

    def show_info(self):
        category = self.category_var.get()
        selected_index = self.device_listbox.curselection()

        if not category or len(selected_index) == 0:
            return

        self.current_info.clear()
        self.info_text.delete(1.0, tk.END)

        for i in selected_index:

            selected_switch = self.switches[i]
            host_ip = self.device_listbox.get(i)
            info, hostname = selected_switch.perform_checks(category)

            self.info_text.insert(tk.END, f"Results for {selected_switch.host} in {category}\n" + self.listToString(info))

            self.current_info.append((info, host_ip, hostname, category))

    def upload_answers(self):
        file_path = filedialog.askopenfilename(title="Select Answers File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_label.config(text = f"{file_path}")

    def check_info(self):
        if len(self.current_info) == 0 or self.file_label.cget("text") == "None":
            return

        path_file = self.file_label.cget("texxt")
        print(path_file)



    def listToDF(self, lst):
        rows = []

        for pair in lst:
            host_ip = pair[1]
            hostname = pair[2]
            category = pair[3]
            for element in pair[0]:
                new_row = {"host_ip": host_ip, "hostname": hostname, "category": category}
                new_row.update(element)
                rows.append(new_row)

        df = pd.DataFrame(rows)
        return df

    def DFtoCSV(self, df, filename):
        df.to_csv(f"C:\\Users\\77782\Desktop\SDU\\3 course\cisco\\finalProject\csv\{filename}")

    def save_info(self):
        if self.current_info == "":
            return
        df = self.listToDF(self.current_info)
        self.DFtoCSV(df, "result.csv")


def main():
    root = tk.Tk()
    app = NetworkTester(root)
    root.mainloop()


if __name__ == "__main__":
    main()
