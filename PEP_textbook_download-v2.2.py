import requests
import os
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import shutil
import sys

def download_images(page, ID, code):
    # 新建文件夹用于保存图片
    if not os.path.exists("images"):
        os.makedirs("images")
    # 创建进度条
    progress_bar['maximum'] = page
    progress_bar['value'] = 0

    # 下载图片并保存
    for a in range(page):
        url = "https://book.pep.com.cn/"+ID+"/files/mobile/"+str(a+1)+".jpg?"+code
        res = requests.get(url=url)
        with open(os.path.join("images", str(a+1) + '.jpg'), mode='wb') as f:
            f.write(res.content)
        progress_bar['value'] = a+1
        window.update()

    messagebox.showinfo("提示", "图片下载完成。")

def convert_to_pdf(pdf_path):
    # 切换到保存图片的目录
    os.chdir("images")

    cwd = os.getcwd()


    # 筛选 JPG 文件并排除没有扩展名的文件
    file_list = [file for file in os.listdir(cwd)
                 if os.path.isfile(os.path.join(cwd, file)) and file.endswith(".jpg")]

    # 根据文件名排序（按照数字顺序排序）
    file_list_sorted = sorted(file_list, key=lambda x: int(x.split(".")[0]))

    # 构建文件路径列表
    file_list_sorted_with_path = [os.path.join(cwd, file) for file in file_list_sorted]

    # 打开每个文件并将其转换为 RGB 格式
    image_list = [Image.open(img).convert("RGB") for img in file_list_sorted_with_path]

    # 将第一个图像保存为 PDF，并将其他图像作为附加图像添加到 PDF 中
    if image_list:
        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
        messagebox.showinfo("完成", "PDF 文件已生成。")
        sys.exit()

        # 删除保存图片的目录
        os.chdir("..")
        shutil.rmtree("images")
    else:
        messagebox.showinfo("错误", "没有找到要处理的图像文件。")
        sys.exit()


def start_conversion():
    global progress_bar
    page = int(entry_page.get())
    ID = entry_ID.get()
    code = entry_code.get()

    messagebox.showinfo("提示", f"页数:{page}\n网站ID：{ID}\n校验码：{code}")

    # 创建进度条
    progress_bar = ttk.Progressbar(window, mode='determinate', length=200)
    progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

    # 下载图片并转换为PDF
    try:
        download_images(page, ID, code)
        # 显示保存文件对话框，并设置标题
        pdf_path = filedialog.asksaveasfilename(defaultextension='.pdf', title='请选择PDF文件保存的位置', filetypes=[('Adobe PDF 文档', '*.pdf')])
        if pdf_path:
            window.withdraw()
            # 指定 PDF 文件的完整路径
            convert_to_pdf(pdf_path)
    except Exception as e:
        messagebox.showinfo("错误", f"发生错误：{str(e)}")
    sys.exit()

# 创建窗口
window = tk.Tk()
window.title("请输入")

# 添加标签和输入框
label_page = tk.Label(window, text="页数:")
label_page.grid(row=0, column=0, padx=5, pady=5)
entry_page = tk.Entry(window)
entry_page.grid(row=0, column=1, padx=5, pady=5)

label_ID = tk.Label(window, text="网站ID:")
label_ID.grid(row=1, column=0, padx=5, pady=5)
entry_ID = tk.Entry(window)
entry_ID.grid(row=1, column=1, padx=5, pady=5)

label_code = tk.Label(window, text="校验码:")
label_code.grid(row=2, column=0, padx=5, pady=5)
entry_code = tk.Entry(window)
entry_code.grid(row=2, column=1, padx=5, pady=5)

# 添加按钮
convert_button = tk.Button(window, text="开始操作", command=start_conversion)
convert_button.grid(row=4, column=0, columnspan=2, pady=10)

# 运行窗口主循环
window.mainloop()
