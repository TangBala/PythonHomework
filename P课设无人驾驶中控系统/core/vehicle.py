# core/vehicle.py
from core.subsystems.air_conditioner import AirConditioner
from core.subsystems.battery import Battery
from core.subsystems.door_window import DoorWindow
from core.subsystems.light import Light  # <--- 确认这一行存在且没有错误
from core.subsystems.navigation import Navigation
# from core.subsystems.battery import Battery # 将来添加
# from core.subsystems.navigation import Navigation # 将来添加

class Vehicle:

    def __init__(self, make="HUST", model="AutopilotSystem"):
        self.make = make
        self.model = model
        self.speed = 0
        self.engine_on = False
        
        # 驾驶模式，模仿你的枚举类型
        self.DRIVING_MODES = ["手动模式", "辅助模式", "自动模式"]
        self.current_driving_mode = self.DRIVING_MODES[0]

        # 初始化并“装配”各个子系统
        self.ac = AirConditioner()
        self.battery = Battery()
        self.door_window = DoorWindow()
        self.light = Light()
        self.navigation = Navigation()
    def toggle_engine(self):  # <--- 确保这个方法的名字是 toggle_engine
        """启动或关闭引擎。"""
        self.engine_on = not self.engine_on
        if self.engine_on:
            print("引擎已启动。")
        else:
            self.speed = 0
            print("引擎已关闭，车速归零。")

    def set_driving_mode(self, mode_index):
        """设置驾驶模式"""
        if 0 <= mode_index < len(self.DRIVING_MODES):
            self.current_driving_mode = self.DRIVING_MODES[mode_index]
            print(f"驾驶模式已切换为: {self.current_driving_mode}")
        else:
            print("无效的驾驶模式。")
    
    def display_main_dashboard(self):
        """显示主仪表盘信息 (代替C的主界面)"""
        engine_status = "运行中" if self.engine_on else "已关闭"
        print("\n======== 无人驾驶中控仪表系统 ========")
        print(f" 车辆: {self.make} {self.model}")
        print(f" 引擎状态: {engine_status}")
        print(f" 当前车速: {self.speed} km/h")
        print(f" 当前驾驶模式: {self.current_driving_mode}")
        print("========================================")
        
        # --- 统一调用各子系统的状态显示 ---
        # 把这些子系统的状态显示也加回来
        self.battery.display_status(show_header=True)
        self.ac.display_status(show_header=True)
        self.light.display_status(show_header=True)
        self.door_window.display_status(show_header=True)
        self.navigation.display_route()