# todo.py 待办清单 最简版 v1
# 功能： 添加代办 + 查看清单

todos = []

while True:
    print("\n===待办清单===")
    print("1、添加代办")
    print("2、查看清单")
    print("0、退出")
    
    choice = input("请选择操作：")
    
    if choice == "1":
        new_todo = input("请输出代办内容：")
        todos.append(new_todo)
        print("已添加！")
        
    elif choice == "2":
        if not todos:
            print("清单是空的")
        else:
            for i, todo in enumerate(todos):
                print(f"{i + 1}.{todo}")
    elif choice == "0":
        print("bye")
        break
    
    else:
        print("无效输出，请重新选择")