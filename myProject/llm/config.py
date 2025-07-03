class APIConfig:
    def __init__(self, 
                 api_key="sk-QGEkpTzYOdG6jkOtTR2UIpR09XINClFMG77POafAefkknppB",
                 model="gpt-3.5-turbo",  # 使用更高级的模型
                 api_base="https://api.chatanywhere.tech",
                 api_type="openai"):
        """
        初始化API配置
        
        参数:
            api_key: API密钥
            model: 使用的模型名称
            api_base: API基础URL
            api_type: API类型 ('openai' 或 'custom')
        """
        self.api_key = api_key
        self.model = model
        self.api_base = api_base
        self.api_type = api_type