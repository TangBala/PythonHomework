# main.py

import os
from core.vehicle import Vehicle

def clear_screen():
    """清空终端屏幕，以获得更好的显示效果。"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(car):
    """显示主菜单并处理用户输入。"""
    while True:
        clear_screen()
        car.display_main_dashboard()
        
        print("\n---【主菜单】---")
        print("1. 启动/关闭引擎")
        print("2. 切换驾驶模式")
        print("3. 空调控制")
        print("4. 灯光控制")
        print("5. 门窗控制")
        print("6. 电池与充电")
        print("7. 导航")
        print("q. 退出程序")
        
        choice = input("\n请选择要操作的模块: ")

        if choice == '1':
            car.toggle_engine()
        elif choice == '2':
            try:
                mode = int(input("请输入模式 (0:手动, 1:辅助, 2:自动): "))
                car.set_driving_mode(mode)
            except ValueError:
                print("输入无效，请输入数字。")
        elif choice == '3':
            # 这里添加一个空调子菜单
            print("进入空调控制...")
            car.ac.turn_on() # 示例：直接打开空调
            temp = int(input("请输入要设定的温度 (16-30): "))
            car.ac.set_temperature(temp)
        elif choice == '4':
            car.light.toggle_headlights() # 示例：直接开关大灯
        elif choice == '5':
            car.door_window.toggle_door_locks() # 示例：直接开关门锁
        elif choice == '6':
            print("进入电池管理...")
            mode = int(input("请选择充电模式 (1:充满, 2:养护): "))
            car.battery.set_mode(mode)
            car.battery.toggle_charging() # 开始充电模拟
        elif choice == '7':
            print("--- 导航菜单 ---")
            print("可选地点:", ", ".join(car.navigation.locations))
            start = input("请输入起点: ")
            end = input("请输入终点: ")
            if car.navigation.set_points(start, end):
                car.navigation.plan_route()
        elif choice.lower() == 'q':
            print("感谢使用，程序已退出。")
            break
        else:
            print("无效的输入，请重新选择。")
        
        input("\n按回车键继续...")

def main():
    """程序主入口。"""
    my_car = Vehicle()
    input("车辆初始化完成，按回车进入主菜单...")
    main_menu(my_car)

if __name__ == "__main__":
    main()