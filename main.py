import tkinter as tk
from tkinter import filedialog, messagebox
from aip import AipOcr

# ================= 配置区 =================
# ！！！请替换为你自己在百度AI平台创建应用的凭证！！！
APP_ID = '122629666'
API_KEY = 'mOe9mcaCm4ckjnKEHwQNPR7m'
SECRET_KEY = '1KnxCSjRgqMtRpALiGAI7UoaZMeAJFY0'
# ==========================================

# 初始化AipOcr对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    """读取本地图片文件"""
    with open(filePath, 'rb') as fp:
        return fp.read()


def select_image():
    """打开文件对话框选择图片"""
    file_path = filedialog.askopenfilename(
        title="选择待识别的图片",
        filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        # 更新输入框显示的路径
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
        # 触发识别逻辑
        recognize_text(file_path)


def recognize_text(file_path):
    """调用百度API进行文字识别"""
    try:
        # 清空之前的文本，提示正在识别
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "正在呼叫百度AI接口，请稍候...\n")
        root.update()  # 强制刷新GUI

        # 读取图片并调用接口
        image = get_file_content(file_path)
        """ 调用通用文字识别, 图片参数为本地图片 """
        result = client.basicGeneral(image)

        # 解析返回的JSON结果
        if 'words_result' in result:
            result_text.delete(1.0, tk.END)
            for word_info in result['words_result']:
                result_text.insert(tk.END, word_info['words'] + '\n')
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"识别失败: {result.get('error_msg', '未知错误')}")

    except Exception as e:
        messagebox.showerror("系统错误", f"发生异常: {str(e)}\n请检查网络或API密钥是否正确！")


# ================= GUI 界面构建 =================
root = tk.Tk()
root.title("智能桌面 OCR 提取工具 - 百度AI版")
root.geometry("550x450")

# 顶部操作区
frame_top = tk.Frame(root)
frame_top.pack(pady=15)

tk.Label(frame_top, text="图片路径:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
path_entry = tk.Entry(frame_top, width=35, font=("微软雅黑", 10))
path_entry.pack(side=tk.LEFT, padx=10)

btn_select = tk.Button(frame_top, text="📂 选择图片并识别", bg="#4CAF50", fg="white",
                       font=("微软雅黑", 10, "bold"), command=select_image)
btn_select.pack(side=tk.LEFT)

# 底部结果展示区
tk.Label(root, text="识别结果:", font=("微软雅黑", 10, "bold")).pack(anchor="w", padx=20)
result_text = tk.Text(root, wrap=tk.WORD, width=65, height=20, font=("微软雅黑", 10))
result_text.pack(pady=5, padx=20)

# 启动主循环
root.mainloop()