import llm_client
import config

original_prompt = "编程指导老师"
new_prompt = """
提供专业的编程教学指导，包括：  
1. 编程语言选择建议  
2. 学习路径规划  
3. 推荐学习资源（书籍/课程/工具）  
4. 项目实践建议  
5. 常见问题解答

请根据学习者的基础水平（初级/中级/高级）和具体需求进行个性化指导。
"""

user_prompt = "我是文科生，我想学习java。"

new_config = config.APIConfig()

# result = llm_client.optimize_prompt_in_llm(original_prompt=original_prompt, config=new_config)
# print(result)

answer1 = llm_client.prompt_test(original_prompt, user_prompt, config=new_config)
print("\n原始提示词测试结果:")
print("=" * 50)
print(answer1)

answer2 = llm_client.prompt_test(new_prompt, user_prompt, config=new_config)
print("\n优化提示词测试结果:")
print("=" * 50)
print(answer2)