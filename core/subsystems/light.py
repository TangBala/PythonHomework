# core/subsystems/light.py

from core.utils import load_data, save_data

class Light:
    """负责管理车辆照明系统的类。"""
    
    MAX_INTERIOR_LEVEL = 5

    def __init__(self):
        """初始化照明系统，从文件加载状态。"""
        print("初始化照明系统中...")
        initial_state = load_data('light.json') or {
            "headlights_on": False,
            "fog_lights_on": False,
            "interior_light_level": 2
        }
        self.headlights_on = initial_state.get('headlights_on', False)
        self.fog_lights_on = initial_state.get('fog_lights_on', False)
        self.interior_light_level = initial_state.get('interior_light_level', 2)
        print("照明系统初始化完成。")

    def toggle_headlights(self):
        """切换前大灯状态。"""
        self.headlights_on = not self.headlights_on
        status_text = "开启" if self.headlights_on else "关闭"
        print(f"前大灯已 {status_text}。")
        self.save_state()

    def toggle_fog_lights(self):
        """切换雾灯状态。"""
        self.fog_lights_on = not self.fog_lights_on
        status_text = "开启" if self.fog_lights_on else "关闭"
        print(f"雾灯已 {status_text}。")
        self.save_state()

    def set_interior_light_level(self, level):
        """设置车内灯光亮度。"""
        if 0 <= level <= self.MAX_INTERIOR_LEVEL:
            self.interior_light_level = level
            print(f"车内灯光亮度已设置为: {level}")
            self.save_state()
        else:
            print(f"错误：无效的亮度等级 (0-{self.MAX_INTERIOR_LEVEL})。")

    def display_status(self, show_header=True):
        """显示当前照明状态。"""
        if show_header:
            print("\n--- 照明状态 ---")
        headlight_status = "开启" if self.headlights_on else "关闭"
        fog_light_status = "开启" if self.fog_lights_on else "关闭"
        print(f"  前大灯: {headlight_status}")
        print(f"  雾灯: {fog_light_status}")
        print(f"  车内灯亮度: {self.interior_light_level}/{self.MAX_INTERIOR_LEVEL}")
        if show_header:
            print("------------------")

    def save_state(self):
        """将当前状态保存到文件。"""
        state = {
            "headlights_on": self.headlights_on,
            "fog_lights_on": self.fog_lights_on,
            "interior_light_level": self.interior_light_level
        }
        save_data(state, 'light.json')

# --- 单元测试 ---
if __name__ == '__main__':
    print("--- 开始照明模块单元测试 ---")
    light_system = Light()
    light_system.display_status()

    print("\n>>> 操作: 打开前大灯")
    light_system.toggle_headlights()

    print("\n>>> 操作: 将内部灯光调到最亮")
    light_system.set_interior_light_level(5)
    light_system.display_status()
    print("--- 照明模块单元测试结束 ---")