# todo.py 待办清单 最简版 v1
# 功能： 添加代办 + 查看清单

todos = []

while True:
    print("\n==== 待办清单 ====")
    print("1. 添加待办")
    print("2. 查看清单")
    print("3. 删除待办")
    print("4. 标记完成")
    print("0. 退出")

    choice = input("请选择操作：")

    if choice == "1":
        new_todo = input("请输出代办内容：")
        todos.append({"text": new_todo, "done": False})
        print("已添加！")

    elif choice == "2":
        if not todos:
            print("清单是空的")
        else:
            for i, todo in enumerate(todos):
                mark = "✅" if todo["done"] else " "
                print(f"{i + 1}.[{mark}]{todo['text']}")

    elif choice == "3":
        if not todos:
            print("清单是空的，没有可删除的")
        else:
            for i, todo in enumerate(todos):
                mark = "✅" if todo["done"] else " "
                print(f"{i + 1}.[{mark}]{todo['text']}")

            num_str = input("请输入要删除的编号：")
            try:
                num = int(num_str)
            except ValueError:
                print("请输入数字")
                continue

            if 1 <= num <= len(todos):
                removed = todos.pop(num - 1)
                print(f"已删除：{removed['text']}")
            else:
                print("编号无效")
                
    elif choice == "4":
        if not todos:
            print("清单是空的")
        else:
            for i, todo in enumerate(todos):
                mark = "✅" if todo["done"] else " "
                print(f"{i + 1}.[{mark}]{todo['text']}")
                
            num_str = input("输入要标记完成的编号：")
            try:
                num = int(num_str)
            except ValueError:
                print("请输入数字")
                continue
            if 1 <= num <= len(todos):
                todos[num - 1]["done"] = True
                print(f"已标记完成：{todos[num - 1]['text']}")
            else:
                print("编号无效")
            
    elif choice == "0":
        print("bye")
        break

    else:
        print("无效输出，请重新选择")
