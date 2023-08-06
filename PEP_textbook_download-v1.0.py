_author_="掠夺の者"
import requests
import os
from PIL import Image

page = int(input("输入页数:"))
ID = input("输入网站ID:")
code = input('输入末尾校验码:')
pdf_name = input("请输入要生成的PDF文件名:")+'.pdf'
print("请稍等,一切交给我(～￣▽￣)～")
# 新建文件夹用于保存图片
if not os.path.exists("images"):
    os.makedirs("images")

# 下载图片并保存
for a in range(page):
    url = "https://book.pep.com.cn/"+ID+"/files/mobile/"+str(a+1)+".jpg?"+code
    res = requests.get(url=url)
    with open(os.path.join("images", str(a+1) + '.jpg'), mode='wb') as f:
        f.write(res.content)
print('别着急，正在生成PDF文件•̀ ω •́ ✧')
# 切换到保存图片的目录
os.chdir("images")

cwd = os.getcwd()
print("当前工作目录：", cwd)

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
    image_list[0].save(pdf_name, save_all=True, append_images=image_list[1:])
    print("PDF 文件已生成。")
else:
    print("没有找到要处理的图像文件。")
endの询问 = input("所有都处理完成啦●'◡'●,按回车键以继续~")
