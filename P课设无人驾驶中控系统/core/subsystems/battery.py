# core/subsystems/battery.py

import time
from core.utils import load_data, save_data

class Battery:
    """
    负责管理车辆电池系统的类。
    包含了电量、充电模式、充电动效等逻辑。
    """
    # 将C代码中的模式用更清晰的方式定义
    MODES = {
        1: "电池充满模式",
        2: "电池养护模式"
    }

    def __init__(self):
        """初始化电池系统，从文件加载状态或使用默认值。"""
        print("初始化电池系统中...")
        # 优先从 a.json 加载状态
        initial_state = load_data('battery.json')
        if initial_state:
            self.capacity = initial_state.get('capacity', 80)
            self.mode_index = initial_state.get('mode_index', 1)
            self.is_charging = initial_state.get('is_charging', False)
        else:
            # 如果文件不存在，则使用默认值
            self.capacity = 80
            self.mode_index = 1
            self.is_charging = False
        
        # 确保模式索引有效
        if self.mode_index not in self.MODES:
            self.mode_index = 1
            
        self.mode = self.MODES[self.mode_index]
        print("电池系统初始化完成。")

    def set_mode(self, mode_index):
        """
        设置充电模式。
        对应C代码中BatteryMouse函数里对模式的选择。
        """
        if mode_index in self.MODES:
            self.mode_index = mode_index
            self.mode = self.MODES[mode_index]
            print(f"电池模式已切换为: {self.mode}")
            self.save_state()
        else:
            print(f"错误：无效的模式索引 {mode_index}")

    def toggle_charging(self):
        """
        切换充电状态（开始/停止）。
        对应C代码中BatteryMouse函数里对充电按钮的点击。
        """
        self.is_charging = not self.is_charging
        if self.is_charging:
            print("电池开始充电...")
            self.simulate_charging_cycle()
        else:
            # 在实际应用中，手动停止充电的逻辑会在这里
            print("充电已手动停止。")
        self.save_state()

    def simulate_charging_cycle(self):
        """
        模拟充电过程。
        这是对C代码中BatteryPlus功能的Python实现。
        """
        if not self.is_charging:
            return

        target_capacity = 100 if self.mode_index == 1 else 80
        print(f"充电目标: {target_capacity}%")

        if self.capacity >= target_capacity:
            print("电量已达到或超过目标，无需充电。")
            self.is_charging = False
            self.save_state()
            return

        while self.capacity < target_capacity:
            self.capacity += 1
            self.display_status(show_header=False) # 实时更新状态
            time.sleep(0.1) # 用短暂的暂停来模拟充电过程
        
        self.is_charging = False
        print(f"\n充电完成！当前电量: {self.capacity}%")
        self.save_state()
        
    def display_status(self, show_header=True):
        """
        显示当前电池状态。
        代替C代码中所有Draw...函数，用文本方式呈现信息。
        """
        if show_header:
            print("\n--- 电池状态 ---")
        
        charge_status = "正在充电" if self.is_charging else "未充电"
        
        # 制作一个简单的文本进度条（使用ASCII字符以避免控制台编码问题）
        progress = int(self.capacity / 10)
        bar = '#' * progress + '.' * (10 - progress)

        print(f"  电量: |{bar}| {self.capacity}%")
        print(f"  模式: {self.mode}")
        print(f"  状态: {charge_status}")
        
        if show_header:
            print("------------------")

    def save_state(self):
        """将当前电池状态保存到 a.json 文件。"""
        state = {
            "capacity": self.capacity,
            "mode_index": self.mode_index,
            "is_charging": self.is_charging
        }
        save_data(state, 'battery.json')

# --- 单元测试 ---
# 这个部分的代码只有在直接运行 battery.py 时才会执行
# 让我们来测试一下这个模块是否能独立工作
if __name__ == '__main__':
    print("--- 开始电池模块单元测试 ---")
    
    # 1. 创建一个电池对象，它会自动从 a.json 加载状态
    my_battery = Battery()
    
    # 2. 显示初始状态
    my_battery.display_status()
    
    # 3. 模拟用户切换到“养护模式”
    print("\n>>> 操作: 切换到养护模式 (模式2)")
    my_battery.set_mode(2)
    my_battery.display_status()
    
    # 4. 模拟用户点击充电按钮
    print("\n>>> 操作: 开始充电...")
    # 注意：在我们的新设计中，toggle_charging()会直接调用充电模拟
    my_battery.toggle_charging() 
    
    # 5. 充电完成后，显示最终状态
    print("\n--- 电池模块单元测试结束 ---")
    my_battery.display_status()