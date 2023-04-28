
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# pyinstaller -F -i 1.ico -w rename.py
# 或者点击compile.bat编译，编译完在dist文件夹里

def rename(folder_path, c1, c2):
    renamed_files = []
    for file_name in os.listdir(folder_path):
        if c1 in file_name:
            new_file_name = file_name.replace(c1, c2)
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {old_file_path} to {new_file_path}")
            renamed_files.append((old_file_path, new_file_path))
    return renamed_files

def choose_folder():
    selected_folder = filedialog.askdirectory(initialdir=".")
    if selected_folder:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, selected_folder)

def show_output(output):
    output_window = tk.Toplevel(window)
    output_window.title("Renamed history")
    
    output_text = tk.Text(output_window, wrap=tk.WORD)
    output_text.insert(tk.END, output)
    output_text.config(state=tk.DISABLED)
    
    close_button = ttk.Button(output_window, text="Close", command=output_window.destroy)
    
    output_text.pack(expand=True, fill=tk.BOTH)
    close_button.pack()

def on_confirm():
    folder_path = folder_path_entry.get()
    output = ""

    for entry in entries:
        c1 = entry[0].get()
        c2 = entry[1].get()
        if folder_path and c1:
            renamed_files = rename(folder_path, c1, c2)
            for old_file_path, new_file_path in renamed_files:
                output += f"Renamed {old_file_path} to {new_file_path}\n"

    if output:
        output += "\n文件重命名成功！"
        show_output(output)
    else:
        show_output("没有重命名任何文件。")

def on_cancel():
    window.destroy()

# 窗口参数
window = tk.Tk()

column_count = 2 # 列数 2
row_count = 13 # 行数 11

window_width = 360
window_height = 320

window.minsize(window_width, window_height)
window.maxsize(600, 360)
window.title("批量重命名工具 Rename Tool")

# 创建两个frame
top_frame = ttk.Frame(window) # 选择文件夹
bottom_frame = ttk.Frame(window) # 其他行

# 把两个frame按网格填充到window中
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=row_count)
window.columnconfigure(0, weight=1)

# 选择文件夹grid权重调整
for i in range(3):
    top_frame.columnconfigure(i, weight=1)

# 其他行
for i in range(column_count):  # 为 3 列分配权重
    bottom_frame.columnconfigure(i, weight=1)

for i in range(row_count):  # 为 9 行分配权重
    bottom_frame.rowconfigure(i, weight=1)

# 选择文件夹 Frame
folder_path_label = tk.Label(window, text="文件夹路径 ")
folder_path_entry = tk.Entry(window)
folder_path_entry.insert(0, ".\\")
choose_folder_button = ttk.Button(window, text="选择文件夹", command=choose_folder)

folder_path_label.grid(in_=top_frame, row=0, column=0, sticky="e")
folder_path_entry.grid(in_=top_frame, row=0, column=1, sticky="ew")
choose_folder_button.grid(in_=top_frame, row=0, column=2, sticky="w")

#其他行 Frame
source_label = tk.Label(window, text="源文字")
replace_label = tk.Label(window, text="替换为")
source_label.grid(in_=bottom_frame, row=0, column=0, sticky="ew")
replace_label.grid(in_=bottom_frame, row=0, column=1, sticky="ew")

# 预设关键词
default_renames = [
    ("psb", ""),
    ("IMG_", ""),
    ("IMG", ""),
    ("mmexport", "")
]

# 其他行 Frame
entries = []
for i, (c1, c2) in enumerate(default_renames, start=1):
    entry1 = tk.Entry(window)
    entry1.insert(0, c1)
    entry2 = tk.Entry(window)
    entry2.insert(0, c2)
    entry1.grid(in_=bottom_frame, row=i, column=0, sticky="ew")
    entry2.grid(in_=bottom_frame, row=i, column=1, sticky="ew")
    entries.append((entry1, entry2))

for i in range(5, row_count-1):
    entry1 = tk.Entry(window)
    entry2 = tk.Entry(window)
    entry1.grid(in_=bottom_frame, row=i, column=0, sticky="ew")
    entry2.grid(in_=bottom_frame, row=i, column=1, sticky="ew")
    entries.append((entry1, entry2))

confirm_button = ttk.Button(window, text="确定", command=on_confirm)
cancel_button = ttk.Button(window, text="取消", command=on_cancel)
confirm_button.grid(in_=bottom_frame, row=row_count, column=0)
cancel_button.grid(in_=bottom_frame, row=row_count, column=1)

window.mainloop()