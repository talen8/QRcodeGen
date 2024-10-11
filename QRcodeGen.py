from io import BytesIO
import time
from tkinter import colorchooser
import qrcode
import tkinter as tk
from PIL import Image, ImageTk
import os
import requests

# 定义常量
WINDOW_TITLE = "QR生成器 - Flec"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
PREVIEW_SIZE = 400
DEFAULT_TEXT = "https://talen.top/"
SAVE_FOLDER = "qrcode/"
WINDOW_ICON = "https://txycos.talen.top/1716712986.ico"

# 检查SAVE_FOLDER目录是否存在，不存在则创建
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# 定义生成二维码函数
def generate_qr_code():
    """生成二维码"""
    global img
    data = text_entry.get()
    if not data.strip():
        status_label.config(text="输入内容不能为空！")
        return
    if len(data) > 200:
        status_label.config(text="输入内容不能超过200个字符！")
        return
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img = img.resize((PREVIEW_SIZE, PREVIEW_SIZE))
    img_preview = ImageTk.PhotoImage(img)
    preview_label.config(image=img_preview)
    preview_label.image = img_preview
    save_button.config(state="normal")
    status_label.config(text="二维码生成成功！")

# 定义保存二维码函数
def save_qr_code():
    """保存二维码"""
    global img
    timestamp = int(time.time())
    filename = f"qrcode_{timestamp}.png"
    full_path = f"{SAVE_FOLDER}{filename}"
    try:
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)
        img.save(full_path)
        status_label.config(text="二维码保存成功！")
    except Exception as e:
        status_label.config(text=f"保存失败！错误信息：{e}")

# 创建主窗口
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
# 图标
icon_url = WINDOW_ICON
response = requests.get(icon_url)
icon_data = response.content
icon_image = Image.open(BytesIO(icon_data))
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# 创建输入提示
text_label = tk.Label(root, text="请输入文本或链接：", font=("微软雅黑", 12), fg="#333")
text_label.pack(pady=(10, 0))

# 创建输入框
text_entry = tk.Entry(root, width=70, font=("微软雅黑", 12), fg="#333", bd=2, relief="ridge")
text_entry.pack(pady=10)
text_entry.insert(0, DEFAULT_TEXT)

# 输入框焦点事件处理函数
def on_focusin(event):
    if text_entry.get() == DEFAULT_TEXT:
        text_entry.delete(0, tk.END)

def on_focusout(event):
    if text_entry.get() == "":
        text_entry.insert(0, DEFAULT_TEXT)

# 绑定输入框焦点事件
text_entry.bind("<FocusIn>", on_focusin)
text_entry.bind("<FocusOut>", on_focusout)

# 鼠标点击事件处理函数
def on_click(event):
    widget = root.winfo_containing(event.x_root, event.y_root)
    if widget!= text_entry:
        if text_entry == root.focus_get():
            root.focus_set()

# 绑定鼠标点击事件
root.bind("<1>", on_click)

# 创建颜色选择变量
fill_color_var = tk.StringVar()
fill_color_var.set("black")
back_color_var = tk.StringVar()
back_color_var.set("white")

# 创建操作按钮容器
button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 10))

# 创建生成二维码按钮
generate_button = tk.Button(button_frame, text="生成", command=generate_qr_code, font=("微软雅黑", 12), fg="#333", bg="#f0f0f0", bd=2, relief="ridge")
generate_button.pack(side=tk.LEFT, padx=10, pady=10)

# 创建保存二维码按钮
save_button = tk.Button(button_frame, text="保存", command=save_qr_code, state="disabled", font=("微软雅黑", 12), fg="#333", bg="#f0f0f0", bd=2, relief="ridge")
save_button.pack(side=tk.LEFT, padx=10, pady=10)

# 创建设置按钮
def open_setting_window():
    setting_window = tk.Toplevel(root)
    setting_window.title("设置")
    setting_window.geometry("400x300")
    setting_window.configure(bg="#f0f0f0")
    setting_window.iconphoto(False, icon_photo)

    def choose_color(color_var, button):
        """选择颜色"""
        color = colorchooser.askcolor()[1]
        color_var.set(color)
        button.config(bg=color)  # 更新按钮颜色
        generate_qr_code()  # 生成新的二维码并更新预览
        setting_window.focus_force()

    def confirm():
        global SAVE_FOLDER
        SAVE_FOLDER = save_folder_entry.get()
        setting_window.destroy()

    def cancel():
        fill_color_var.set("black")
        back_color_var.set("white")
        generate_qr_code()
        setting_window.destroy()

    color_frame = tk.Frame(setting_window, bg="#f0f0f0")
    color_frame.pack(fill="x", padx=50, pady=20)
    tk.Label(color_frame, text="颜色：", bg="#f0f0f0", font=("微软雅黑", 12)).pack(side="left")
    color_button = tk.Button(color_frame, bg=fill_color_var.get(), width=5, command=lambda: choose_color(fill_color_var, color_button))
    color_button.pack(side="left")

    back_color_frame = tk.Frame(setting_window, bg="#f0f0f0")
    back_color_frame.pack(fill="x", padx=50, pady=20)
    tk.Label(back_color_frame, text="背景：", bg="#f0f0f0", font=("微软雅黑", 12)).pack(side="left")
    back_color_button = tk.Button(back_color_frame, bg=back_color_var.get(), width=5, command=lambda: choose_color(back_color_var, back_color_button))
    back_color_button.pack(side="left")

    save_folder_frame = tk.Frame(setting_window, bg="#f0f0f0")
    save_folder_frame.pack(fill="x", padx=50, pady=20)
    tk.Label(save_folder_frame, text="默认保存路径：", bg="#f0f0f0", font=("微软雅黑", 12)).pack(side="left")
    global save_folder_entry
    save_folder_entry = tk.Entry(save_folder_frame, width=20, font=("微软雅黑", 12), fg="#333", bd=2, relief="ridge")
    save_folder_entry.pack(side="left")
    save_folder_entry.insert(0, SAVE_FOLDER)

    button_frame = tk.Frame(setting_window, bg="#f0f0f0")
    button_frame.pack(fill="x", padx=50, pady=20)
    tk.Button(button_frame, text="应用设置", command=confirm, font=("微软雅黑", 12), fg="#333", bg="#f0f0f0", bd=2, relief="ridge").pack(side="left", expand=True, fill="x", padx=10)
    tk.Button(button_frame, text="恢复默认", command=cancel, font=("微软雅黑", 12), fg="#333", bg="#f0f0f0", bd=2, relief="ridge").pack(side="left", expand=True, fill="x", padx=10)

setting_button = tk.Button(button_frame, text="设置", command=open_setting_window, font=("微软雅黑", 12), fg="#333", bg="#f0f0f0", bd=2, relief="ridge")
setting_button.pack(side=tk.LEFT, padx=10, pady=10)

# 创建预览
preview_label = tk.Label(root, font=("微软雅黑", 12), fg="#333")
preview_label.pack(pady=10)

# 创建状态标签
status_label = tk.Label(root, text="", font=("微软雅黑", 12), fg="#333")
status_label.pack(pady=10)

# 启动主循环
root.mainloop()
