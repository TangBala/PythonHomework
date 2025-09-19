# core/subsystems/navigation.py

import heapq
from core.utils import load_data

class Navigation:
    """
    负责处理车辆导航、地图信息和路径规划的类。
    核心功能是使用Dijkstra算法计算最短路径。
    """
    def __init__(self):
        """初始化导航系统，加载地图数据。"""
        print("初始化导航系统中...")
        map_data = load_data('map.json')
        if not map_data:
            raise FileNotFoundError("错误: map.json 地图文件未找到或格式错误。")
        
        self.locations = map_data.get('locations', [])
        self.graph = map_data.get('graph', {})
        self.start_point = None
        self.end_point = None
        self.route = None
        self.total_distance = 0
        print("导航系统初始化完成。")

    def set_points(self, start, end):
        """设置导航的起点和终点。"""
        if start not in self.locations:
            print(f"错误：起点 '{start}' 不在地图上。")
            return False
        if end not in self.locations:
            print(f"错误：终点 '{end}' 不在地图上。")
            return False
        
        self.start_point = start
        self.end_point = end
        print(f"导航已设置: 从 {start} 到 {end}")
        return True

    def plan_route(self):
        """
        使用Dijkstra算法规划最短路径。
        这是对C代码 plan.c 中核心算法的Pythonic实现。
        """
        if not self.start_point or not self.end_point:
            print("错误：请先设置起点和终点。")
            return False

        # 1. 初始化距离、前驱节点和优先队列
        distances = {location: float('inf') for location in self.locations}
        distances[self.start_point] = 0
        previous_nodes = {location: None for location in self.locations}
        
        # 优先队列（最小堆）存储 (距离, 节点)
        priority_queue = [(0, self.start_point)]

        # 2. Dijkstra算法主循环
        while priority_queue:
            # 弹出当前距离最小的节点
            current_distance, current_node = heapq.heappop(priority_queue)

            # 如果当前距离已经大于记录的距离，则跳过
            if current_distance > distances[current_node]:
                continue

            # 如果到达终点，则可以提前结束
            if current_node == self.end_point:
                break
            
            # 遍历当前节点的所有邻居
            for neighbor, weight in self.graph.get(current_node, {}).items():
                distance = current_distance + weight
                
                # 如果找到了更短的路径，则更新
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # 3. 回溯路径并保存结果
        path = []
        current = self.end_point
        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]
        
        # 检查路径是否可达
        if path[0] == self.start_point:
            self.route = path
            self.total_distance = distances[self.end_point]
            print("路径规划成功！")
            return True
        else:
            self.route = None
            self.total_distance = float('inf')
            print("错误：无法找到从起点到终点的路径。")
            return False
            
    def display_route(self):
        """以文本方式显示规划好的路线信息。"""
        print("\n--- 导航路线 ---")
        if self.route:
            print(f"  起点: {self.start_point}")
            print(f"  终点: {self.end_point}")
            print(f"  路线: {' -> '.join(self.route)}")
            print(f"  总距离: {self.total_distance} 米")
            # 假设平均速度为30km/h (约8.3m/s)
            estimated_time = self.total_distance / 8.3
            print(f"  预计时间: {estimated_time:.1f} 秒")
        else:
            print("  当前没有规划路线。")
        print("------------------")


# --- 单元测试 ---
if __name__ == '__main__':
    print("--- 开始导航模块单元测试 ---")
    nav_system = Navigation()
    
    # 打印所有可选地点
    print("\n可选地点:")
    print(", ".join(nav_system.locations))
    
    # 1. 设置一个有效路径
    print("\n>>> 操作: 规划从'西操'到'启明楼'的路线")
    nav_system.set_points(start="西操", end="启明楼")
    
    # 2. 进行路径规划
    if nav_system.plan_route():
        # 3. 显示规划结果
        nav_system.display_route()
    
    # 4. 测试一个不可达路径
    print("\n>>> 操作: 规划从'紫菘'到'师生'的路线 (师生为孤立点)")
    nav_system.set_points(start="紫菘", end="师生")
    if not nav_system.plan_route():
        nav_system.display_route()

    print("\n--- 导航模块单元测试结束 ---")