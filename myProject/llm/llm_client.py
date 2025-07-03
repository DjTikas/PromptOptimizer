# llm_client.py
from openai import OpenAI
from llm.config import APIConfig
from llm.prompts import *

async def optimize_prompt_in_llm(original_prompt, config):
    """
    使用大模型优化提示词
    
    参数:
        original_prompt: 原始提示词
        config: APIConfig对象
        
    返回:
        str: 优化后的提示词
    """
    system_message = NORMAL_OPTIMIZE_PROMPT

    if config.api_type == "openai":
        # 使用OpenAI新版API (v1.x)
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.api_base
        )
        
        response = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": original_prompt}
            ],
            temperature=0.5,  
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
def prompt_test(system, prompt, config):
    """
    使用大模型测试优化后的提示词

    参数:
        system: 系统消息
        prompt: 原始提示词
        config: APIConfig对象

    返回:
        str: 测试结果
    """
    if config.api_type == "openai":
        # 使用OpenAI新版API (v1.x)
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.api_base
        )

        response = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  
            max_tokens=500
        )
        return response.choices[0].message.content.strip()