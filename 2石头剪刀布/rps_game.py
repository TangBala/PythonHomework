import random
import time

class RockPaperScissorsGame:
    """
    面向对象的石头剪刀布游戏，支持标准模式和生活大爆炸模式。
    """
    def __init__(self):
        """
        初始化游戏，默认以标准模式开始。
        """
        self.user_score = 0
        self.computer_score = 0
        self.round_count = 0
        
        # 初始设置为标准模式的规则
        self._set_standard_mode()

    def _set_standard_mode(self):
        """设置标准模式的游戏规则、选项和别名。"""
        self.choices = ['rock', 'paper', 'scissors']
        self.rules = {
            'rock': ['scissors'],
            'paper': ['rock'],
            'scissors': ['paper']
        }
        self.aliases = {
            'r': 'rock', 'rock': 'rock',
            'p': 'paper', 'paper': 'paper',
            's': 'scissors', 'scissors': 'scissors'
        }

    def _upgrade_to_spock_lizard(self):
        """
        升级游戏到“生活大爆炸”模式，动态更新规则。
        """
        print("\n--- 游戏升级！欢迎来到石头-剪刀-布-蜥蜴-史波克！ ---")
        print("规则:")
        print("  - 剪刀 剪 布, 剪刀 斩首 蜥蜴")
        print("  - 布 包 石头, 布 证伪 史波克")
        print("  - 石头 砸 蜥蜴, 石头 砸 剪刀")
        print("  - 蜥蜴 毒死 史波克, 蜥蜴 吃掉 布")
        print("  - 史波克 砸碎 剪刀, 史波克 汽化 石头")
        print("----------------------------------------------------\n")

        self.choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        
        # 新的规则：key 克制 value列表中的所有项
        self.rules = {
            'scissors': ['paper', 'lizard'],
            'paper': ['rock', 'spock'],
            'rock': ['lizard', 'scissors'],
            'lizard': ['spock', 'paper'],
            'spock': ['scissors', 'rock']
        }
        
        # 更新别名，增加蜥蜴(l)和史波克(k)
        self.aliases.update({
            'l': 'lizard', 'lizard': 'lizard',
            'k': 'spock', 'spock': 'spock' # 用 'k' 代表 Spock 避免与 scissors 的 's' 冲突
        })

    def _get_user_choice(self):
        """获取并验证用户的输入。"""
        # 动态生成提示信息
        prompt_options = ", ".join([f"{name.capitalize()}({alias})" for alias, name in self.aliases.items() if len(alias) == 1])
        prompt = f"请选择 {prompt_options}，或输入 'q' 退出: "
        
        while True:
            user_input = input(prompt).lower()
            if user_input in ['q', 'quit']:
                return 'quit'
            if user_input in self.aliases:
                return self.aliases[user_input]
            else:
                print("无效输入！请重试。")

    def _get_computer_choice(self):
        """获取计算机的随机选择。"""
        return random.choice(self.choices)

    def _determine_winner(self, user_choice, computer_choice):
        """根据当前规则判断赢家并更新分数。"""
        print(f"\n你选择了: {user_choice.capitalize()}")
        print("电脑正在思考...")
        time.sleep(0.5)
        print(f"电脑选择了: {computer_choice.capitalize()}")
        
        if user_choice == computer_choice:
            print("--- 结果: 平局！ ---")
        # 检查电脑的选择是否在用户选择的“克制列表”中
        elif computer_choice in self.rules[user_choice]:
            print("--- 结果: 你赢了！ ---")
            self.user_score += 1
        else:
            print("--- 结果: 电脑赢了！ ---")
            self.computer_score += 1

    def _display_score(self):
        """显示当前的比分。"""
        print("------------------------------")
        print(f"当前比分 -> 你: {self.user_score} | 电脑: {self.computer_score}")
        print("------------------------------\n")
    
    def _play_round(self):
        """进行一个回合的游戏。"""
        user_choice = self._get_user_choice()
        if user_choice == 'quit':
            return False # 返回 False 表示用户想退出
        
        computer_choice = self._get_computer_choice()
        self._determine_winner(user_choice, computer_choice)
        self._display_score()
        return True # 返回 True 表示游戏继续

    def _play_best_of_three(self):
        """进行三局两胜制的游戏。"""
        print("--- 开始标准模式：三局两胜！ ---")
        while self.user_score < 2 and self.computer_score < 2 and self.round_count < 3:
            self.round_count += 1
            print(f"\n--- 第 {self.round_count} 局 ---")
            self._play_round() # 直接调用单回合方法

        print("\n--- 三局两胜结束！ ---")
        if self.user_score > self.computer_score:
            print("恭喜你，你赢得了系列赛！")
        else:
            print("电脑赢得了系列赛！")
    
    def _play_continuous(self):
        """进行无限回合的游戏，直到用户退出。"""
        # 重置分数，开始新模式
        self.user_score = 0
        self.computer_score = 0
        print("\n--- 开始无限挑战模式！ ---")
        self._display_score()
        
        while self._play_round():
            pass # _play_round 返回 True 时循环继续

    def start_game(self):
        """
        游戏的主控制器，管理整个游戏流程。
        """
        self._play_best_of_three()
        
        while True:
            play_upgraded = input("\n想要玩升级的“生活大爆炸版”吗？(y/n): ").lower()
            if play_upgraded in ['y', 'yes']:
                self._upgrade_to_spock_lizard()
                self._play_continuous()
                break # 升级版玩完后游戏结束
            elif play_upgraded in ['n', 'no']:
                break # 用户选择不玩，游戏结束
            else:
                print("无效输入，请输入 'y' 或 'n'。")

        print("\n感谢游玩！")
        print(f"最终得分 -> 你: {self.user_score} | 电脑: {self.computer_score}")

# 主程序入口
if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.start_game()