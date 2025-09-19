# core/subsystems/air_conditioner.py
from core.utils import load_data, save_data

class AirConditioner:
    def __init__(self):
        # 初始化时加载状态，如果文件不存在则使用默认值
        initial_state = load_data('ac.json') or {
            "is_on": False,
            "mode": "auto",  # auto, manual
            "preset_temp": 24,
            "current_temp": 22,
            "preset_humidity": 50,
            "current_humidity": 45
        }
        self.is_on = initial_state['is_on']
        self.mode = initial_state['mode']
        self.preset_temp = initial_state['preset_temp']
        self.current_temp = initial_state['current_temp']
        # ... 其他属性

    def turn_on(self):
        """开启空调"""
        self.is_on = True
        print("空调已开启。")
        self.save_state()

    def turn_off(self):
        """关闭空调"""
        self.is_on = False
        print("空调已关闭。")
        self.save_state()

    def set_temperature(self, temp):
        """设置温度"""
        if 16 <= temp <= 30:
            self.preset_temp = temp
            print(f"空调温度已设置为: {self.preset_temp}°C")
            self.save_state()
        else:
            print("温度设置无效。")
    
    def display_status(self, show_header=True):
        """显示当前状态 (代替C的绘图函数)"""
        status = "开启" if self.is_on else "关闭"
        if show_header:
            print(f"\n--- 空调状态 ---")
        print(f"  状态: {status}")
        print(f"  模式: {self.mode}")
        print(f"  设定温度: {self.preset_temp}°C")
        if show_header:
            print(f"------------------")


    def save_state(self):
        """保存当前状态到文件"""
        state = self.__dict__ # 使用__dict__可以方便地获取所有实例属性
        save_data(state, 'ac.json')