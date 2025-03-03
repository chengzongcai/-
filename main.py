import tkinter as tk
from tkinter import messagebox

class PercentageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("百分比计算器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 设置窗口图标和主题颜色
        self.root.configure(bg="#f0f0f0")
        
        # 窗口置顶状态
        self.is_topmost = False
        
        # 创建标题标签和置顶按钮框架
        self.header_frame = tk.Frame(root, bg="#f0f0f0")
        self.header_frame.pack(fill=tk.X, pady=10)
        
        # 创建标题标签
        self.title_label = tk.Label(
            self.header_frame, 
            text="数值范围计算器", 
            font=("微软雅黑", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # 创建置顶按钮
        self.topmost_button = tk.Button(
            self.header_frame,
            text="置顶窗口",
            font=("微软雅黑", 10),
            bg="#e0e0e0",
            fg="#333333",
            padx=10,
            pady=2,
            bd=1,
            relief=tk.RAISED,
            command=self.toggle_topmost
        )
        self.topmost_button.pack(side=tk.RIGHT, padx=20)
        
        # 创建输入框和标签
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)
        
        self.input_label = tk.Label(
            self.input_frame, 
            text="请输入一个数字:", 
            font=("微软雅黑", 12),
            bg="#f0f0f0"
        )
        self.input_label.pack(side=tk.LEFT, padx=5)
        
        self.input_entry = tk.Entry(
            self.input_frame, 
            font=("微软雅黑", 12),
            width=15,
            bd=2,
            relief=tk.GROOVE
        )
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.focus()
        
        # 添加自动更新状态标签
        self.status_label = tk.Label(
            root,
            text="自动更新已启用 (每0.5秒)",
            font=("微软雅黑", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.status_label.pack(pady=5)
        
        # 创建结果显示框
        self.result_frame = tk.Frame(root, bg="#f0f0f0")
        self.result_frame.pack(pady=10, fill=tk.X, padx=50)
        
        # 上限结果 (现在放在上面)
        self.upper_frame = tk.Frame(self.result_frame, bg="#f0f0f0")
        self.upper_frame.pack(fill=tk.X, pady=5)
        
        self.upper_label = tk.Label(
            self.upper_frame, 
            text="上限 (+10%):", 
            font=("微软雅黑", 12),
            bg="#f0f0f0",
            width=12,
            anchor="w"
        )
        self.upper_label.pack(side=tk.LEFT)
        
        self.upper_result = tk.Label(
            self.upper_frame, 
            text="--", 
            font=("微软雅黑", 12, "bold"),
            bg="#e6e6e6",
            fg="#333333",
            width=15,
            anchor="center",
            relief=tk.GROOVE
        )
        self.upper_result.pack(side=tk.LEFT, padx=5, fill=tk.X)
        
        # 下限结果 (现在放在下面)
        self.lower_frame = tk.Frame(self.result_frame, bg="#f0f0f0")
        self.lower_frame.pack(fill=tk.X, pady=5)
        
        self.lower_label = tk.Label(
            self.lower_frame, 
            text="下限 (-10%):", 
            font=("微软雅黑", 12),
            bg="#f0f0f0",
            width=12,
            anchor="w"
        )
        self.lower_label.pack(side=tk.LEFT)
        
        self.lower_result = tk.Label(
            self.lower_frame, 
            text="--", 
            font=("微软雅黑", 12, "bold"),
            bg="#e6e6e6",
            fg="#333333",
            width=15,
            anchor="center",
            relief=tk.GROOVE
        )
        self.lower_result.pack(side=tk.LEFT, padx=5, fill=tk.X)
        
        # 存储上一次输入的值，用于比较是否有变化
        self.last_input = ""
        
        # 启动自动检测
        self.start_auto_detection()
    
    def toggle_topmost(self):
        """切换窗口置顶状态"""
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        
        # 更新按钮文本和样式
        if self.is_topmost:
            self.topmost_button.config(
                text="取消置顶",
                bg="#4CAF50",
                fg="white",
                relief=tk.SUNKEN
            )
        else:
            self.topmost_button.config(
                text="置顶窗口",
                bg="#e0e0e0",
                fg="#333333",
                relief=tk.RAISED
            )
        
    def start_auto_detection(self):
        """启动自动检测功能，每0.5秒检测一次输入框中的数据"""
        self.check_input_changes()
        
    def check_input_changes(self):
        """检查输入框中的数据是否有变化，如果有则更新计算结果"""
        current_input = self.input_entry.get()
        
        # 如果输入有变化，则进行计算
        if current_input != self.last_input:
            self.last_input = current_input
            self.calculate_range(show_error=False)
            
        # 每0.5秒检测一次
        self.root.after(500, self.check_input_changes)
        
    def calculate_range(self, show_error=True):
        """计算输入数字的上下10%范围"""
        try:
            # 获取输入值并转换为浮点数
            input_text = self.input_entry.get().strip()
            
            # 如果输入为空，则显示默认值
            if not input_text:
                self.lower_result.config(text="--")
                self.upper_result.config(text="--")
                return
                
            input_value = float(input_text)
            
            # 计算上下10%的范围
            lower_bound = input_value * 0.9  # 下限 (减去10%)
            upper_bound = input_value * 1.1  # 上限 (加上10%)
            
            # 更新结果显示
            self.lower_result.config(text=f"{lower_bound:.2f}")
            self.upper_result.config(text=f"{upper_bound:.2f}")
            
        except ValueError:
            # 只有在show_error为True时才显示错误消息
            if show_error:
                messagebox.showerror("输入错误", "请输入有效的数字！")
                self.input_entry.delete(0, tk.END)
                self.input_entry.focus()
            # 输入无效时显示默认值
            self.lower_result.config(text="--")
            self.upper_result.config(text="--")

def main():
    root = tk.Tk()
    app = PercentageCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 