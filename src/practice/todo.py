# todo.py  v5 重构 + 统计
# 清理已完成

import json 

FILE_NAME = "todos.json"

def load_todos():
    """启动时读取文件里的待办，文件不存在就返回空列表"""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def save_todos(todos):
    """把待办写回文件"""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
        
def show_todos(todos):
    if not todos:
        print("清单是空的")
        return False
    for i, todo in enumerate(todos):
        mark = "✓" if todo["done"] else " "
        print(f"{i + 1}. [{mark}] {todo['text']}")
    return True

def get_valid_number(prompt, max_num):
    """让用户输入 1~max_num 之间的编号，非法则重新输入。"""
    while True:
        num_str = input(prompt)
        try:
            num = int(num_str)
        except ValueError:
            print("请输入数字")
            continue
        if 1 <= num <= max_num:
            return num
        print("编号无效，范围是 1-" + str(max_num))

def add_todo(todos):
    new_todo = input("输入待办内容：")
    todos.append({"text": new_todo, "done": False})
    print("已添加！")
    
def delete_todo(todos):
    if not show_todos(todos):
        return
    num = get_valid_number("输入要删除的编号：", len(todos))
    removed = todos.pop(num - 1)
    todos[num - 1]["done"] = True
    print(f"已删除：{removed['text']}")

def mark_done(todos):
    if not show_todos(todos):
        return
    num = get_valid_number("请输入要标记完成的编号：", len(todos))
    todos[num - 1]["done"] = True
    print(f"已标记完成：{todos[num - 1]['text']}")
    
def clean_done(todos):
    before = len(todos)
    todos[:] = [t for t in todos if not t["done"]]
    removed = before - len(todos)
    print(f"已清理{removed}条已完成待办")

def show_stats(todos):
    """统计：总条数、已完成、未完成。"""
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    print(f"总计 {total} 条，已完成 {done} 条，未完成 {total - done} 条")

todos = load_todos()


while True:
    print("\n==== 待办清单 ====")
    print("1. 添加待办")
    print("2. 查看清单")
    print("3. 删除待办")
    print("4. 标记完成")
    print("5. 清理已完成")
    print("6. 统计")
    print("0. 退出")

    choice = input("请选择操作: ")

    if choice == "1":
        add_todo(todos)
        save_todos(todos)
    elif choice == "2":
        show_todos(todos)
    elif choice == "3":
        delete_todo(todos)
        save_todos(todos)
    elif choice == "4":
        mark_done(todos)
        save_todos(todos)
    elif choice == "5":
        clean_done(todos)
        save_todos(todos)
    elif choice == "6":
        show_stats(todos)
    elif choice == "0":
        print("再见!")
        break
    else:
        print("无效输入，请重新选择")