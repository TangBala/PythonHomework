import requests

class CurrencyConverter:
    """
    一个使用ExchangeRate-API的货币转换器类。
    """
    def __init__(self, api_key):
        """
        初始化转换器。
        
        参数:
            api_key (str): 你的ExchangeRate-API密钥。
        """
        self.api_key = api_key
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}"
        self.rates = self._get_rates("USD")  # 初始化时默认加载以美元为基准的汇率

    def _get_rates(self, base_currency):
        """
        一个私有方法，用于从API获取和更新汇率数据。
        """
        url = f"{self.base_url}/latest/{base_currency}"
        try:
            # 发送HTTP GET请求
            response = requests.get(url)
            # 如果请求出现错误 (如404, 500等), 这行代码会抛出异常
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") == "success":
                return data["conversion_rates"]
            else:
                # 处理API返回的特定错误
                print(f"错误: 无法获取汇率 - {data.get('error-type')}")
                return None
        except requests.exceptions.RequestException as e:
            # 处理网络连接等请求错误
            print(f"网络错误: {e}")
            return None

    def convert(self, amount, from_currency, to_currency):
        """
        执行货币转换。

        参数:
            amount (float): 要转换的金额。
            from_currency (str): 源货币代码 (如 "USD")。
            to_currency (str): 目标货币代码 (如 "CNY")。
            
        返回:
            float: 转换后的金额，如果失败则返回None。
        """
        if self.rates is None:
            print("错误: 汇率数据不可用。")
            return None

        if from_currency not in self.rates or to_currency not in self.rates:
            print(f"错误: 不支持的货币代码。请确保 '{from_currency}' 和 '{to_currency}' 是有效的。")
            return None
        
        # 转换公式：金额 * (目标货币汇率 / 源货币汇率)
        # 因为所有汇率都是相对于同一个基准货币（这里是USD）
        rate = self.rates[to_currency] / self.rates[from_currency]
        converted_amount = amount * rate
        
        return converted_amount

def main():
    """
    程序的主函数，处理用户交互。
    """
    # ！！！请务必将这里的字符串替换成你自己的API密钥！！！
    API_KEY = "YOUR_OWN_API_KEY"
    converter = CurrencyConverter(API_KEY)

    # 检查初始化时是否成功获取汇率
    if converter.rates is None:
        print("程序启动失败，无法连接到汇率服务。")
        return

    print("--- 高级货币转换器 ---")
    print("输入 'exit' 退出程序。\n")

    while True:
        try:
            amount_str = input("请输入转换金额 (例如 100): ")
            if amount_str.lower() == 'exit':
                break
            amount = float(amount_str)

            from_currency = input("请输入源货币代码 (例如 USD): ").upper()
            if from_currency.lower() == 'exit':
                break
                
            to_currency = input("请输入目标货币代码 (例如 CNY): ").upper()
            if to_currency.lower() == 'exit':
                break

            result = converter.convert(amount, from_currency, to_currency)

            if result is not None:
                print("---------------------------------")
                print(f"结果: {amount:.2f} {from_currency} = {result:.2f} {to_currency}")
                print("---------------------------------\n")

        except ValueError:
            print("错误: 金额必须是数字。请重试。\n")
        except Exception as e:
            print(f"发生未知错误: {e}\n")

if __name__ == "__main__":
    main()