# core/subsystems/door_window.py

from core.utils import load_data, save_data

class DoorWindow:
    """负责管理车辆门窗系统的类。"""

    WINDOW_POSITIONS = ["front_left", "front_right", "rear_left", "rear_right"]

    def __init__(self):
        """初始化门窗系统，从文件加载状态。"""
        print("初始化门窗系统中...")
        initial_state = load_data('door_window.json') or {
            "doors_locked": True,
            "windows_status": {pos: 0 for pos in self.WINDOW_POSITIONS}
        }
        self.doors_locked = initial_state.get('doors_locked', True)
        self.windows_status = initial_state.get('windows_status', {pos: 0 for pos in self.WINDOW_POSITIONS})
        print("门窗系统初始化完成。")

    def toggle_door_locks(self):
        """切换车门锁状态（上锁/解锁）。"""
        self.doors_locked = not self.doors_locked
        status_text = "上锁" if self.doors_locked else "解锁"
        print(f"所有车门已 {status_text}。")
        self.save_state()
        return self.doors_locked

    def set_window_level(self, position, level):
        """设置单个车窗的打开程度 (0-100)。"""
        if position not in self.WINDOW_POSITIONS:
            print(f"错误：无效的车窗位置 '{position}'")
            return
        if not 0 <= level <= 100:
            print("错误：车窗打开程度必须在 0 到 100 之间。")
            return
            
        self.windows_status[position] = level
        print(f"{position} 车窗已设置为 {level}% 打开。")
        self.save_state()

    def close_all_windows(self):
        """一键关闭所有车窗。"""
        for position in self.windows_status:
            self.windows_status[position] = 0
        print("所有车窗已关闭。")
        self.save_state()

    def display_status(self, show_header=True):
        """显示当前门窗状态。"""
        if show_header:
            print("\n--- 门窗状态 ---")
        lock_status = "已上锁" if self.doors_locked else "已解锁"
        print(f"  车门锁: {lock_status}")
        print("  车窗状态:")
        for pos, level in self.windows_status.items():
            print(f"    - {pos}: {level}% 打开")
        if show_header:
            print("------------------")

    def save_state(self):
        """将当前状态保存到文件。"""
        state = {
            "doors_locked": self.doors_locked,
            "windows_status": self.windows_status
        }
        save_data(state, 'door_window.json')

# --- 单元测试 ---
if __name__ == '__main__':
    print("--- 开始门窗模块单元测试 ---")
    dw_system = DoorWindow()
    dw_system.display_status()

    print("\n>>> 操作: 解锁车门")
    dw_system.toggle_door_locks()
    
    print("\n>>> 操作: 打开左前车窗一半")
    dw_system.set_window_level("front_left", 50)
    dw_system.display_status()

    print("\n>>> 操作: 一键关窗")
    dw_system.close_all_windows()
    dw_system.display_status()
    print("--- 门窗模块单元测试结束 ---")