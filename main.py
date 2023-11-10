import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# 配置和维护的常量
BG_COLOR = "#ddeeff"  # 淡蓝色背景
BUTTON_COLOR = "#336699"  # 深蓝色按钮
TEXT_COLOR = "#ffffff"  # 白色文本
FONT = ("Arial", 12)


MAX_INPUT_SIZE = 128
MAX_DATA_SIZE = 20000

data_rules = {}
num_for_sentence = {}
database = ""
data_deal = ""
grammar_now = 0
position = 0
state_now = '0'
tot_grammar = 0
set_text = ""


def read_from_file(filename):
    global database
    with open(filename, 'r') as file:
        database = file.read()


def initialize_data():
    global tot_grammar, database

    check = 0
    tot_grammar = 1
    little_check = 1
    data_rules[tot_grammar] = []

    for i, char in enumerate(database):
        if char == '\n':
            if i + 1 < len(database) and database[i + 1] == '\n':
                num_for_sentence[tot_grammar] = little_check
                little_check = 0
                tot_grammar += 1
                data_rules[tot_grammar] = []
            else:
                little_check += 1
            continue
        if char == ' ':
            continue

        if len(data_rules[tot_grammar]) < little_check:
            data_rules[tot_grammar].append(['']*5)
        data_rules[tot_grammar][little_check - 1][check] = char

        check += 1
        check %= 5

    num_for_sentence[tot_grammar] = little_check
    print(f"Loaded rules: {data_rules}")


def select_grammar():
    global grammar_now
    grammar_now = simpledialog.askinteger("请选择语法", "1. 0^n1^n\n2. 减法(格式为000100)\n3.wcw,w为{a,b}+\n4.log2 N,an表示输入，bn表示输出\n5.一进制转换为二进制，an表示一进制\n\n请选择语法:")


def read_sentence():
    global data_deal, position, state_now
    sentence = simpledialog.askstring("Input", "输入句子:")
    if not sentence:
        messagebox.showerror("Error", "请输入合法的句子")
        return

    data_deal = 'B' + sentence + 'B'
    position = 1
    state_now = '0'


def execute_rules():
    global data_deal, position, state_now, set_text, grammar_now

    while state_now != '#':
        trigger = 0
        for i, rule in enumerate(data_rules[grammar_now]):
            if rule[0] == state_now and rule[1] == data_deal[position]:
                state_now = rule[2]
                data_deal = data_deal[:position] + rule[3] + data_deal[position+1:]

                if rule[4] == 'R':
                    position += 1
                    if position == len(data_deal) - 1:
                        data_deal += 'B'
                elif rule[4] == 'L':
                    position -= 1
                    if position == len(data_deal) - 1:
                        data_deal += 'B'

                trigger = 1
                break

        if not trigger:
            messagebox.showerror("Error", "不合法的输入")
            return

    set_text = data_deal + '\n' + (' ' * (position)) + '*'
    messagebox.showinfo("Result", set_text)


def main():
    root = tk.Tk()
    root.title("图灵机模拟器")
    root.configure(bg=BG_COLOR)
    root.geometry("800x600")  # 增加窗口大小

    label = tk.Label(root, text="欢迎使用图灵机模拟器", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
    label.pack(pady=20)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(fill='x', padx=50)

    # 创建按钮并设置统一的样式
    buttons = [
        ("加载语法规则", lambda: [read_from_file('in.txt'), initialize_data()]),
        ("选择图灵机功能", select_grammar),
        ("输入你的句子", read_sentence),
        ("开始运行", execute_rules)
    ]
    for (text, command) in buttons:
        button = tk.Button(button_frame, text=text, command=command, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT, height=2, width=20)
        button.pack(pady=10, fill='x', expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()