"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config


class LLMClient:
    """LLM客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        # 部分模型（如MiniMax M2.5）会在content中包含<think>思考内容，需要移除
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content
    
    def _clean_and_parse_json(self, response: str) -> Dict[str, Any]:
        """
        Clean LLM response text and parse as JSON.
        Handles markdown code fences and <think> tags from reasoning models.
        """
        cleaned = response.strip()
        # Remove <think>...</think> blocks (reasoning models like Qwen)
        cleaned = re.sub(r'<think>[\s\S]*?</think>', '', cleaned).strip()
        # Remove markdown code fences
        cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n?```\s*$', '', cleaned)
        cleaned = cleaned.strip()

        return json.loads(cleaned)

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Tries response_format=json_object first. If the provider rejects it
        (e.g. Groq + reasoning models like Qwen that emit <think> tags),
        falls back to plain text mode with a higher token budget and parses
        the JSON manually.
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        import logging
        logger = logging.getLogger(__name__)

        # --- Attempt 1: strict JSON mode ---
        try:
            response = self.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            return self._clean_and_parse_json(response)
        except Exception as json_mode_err:
            logger.warning(
                f"JSON mode failed ({json_mode_err}), retrying without "
                f"response_format..."
            )

        # --- Attempt 2: plain text mode ---
        # For reasoning models (Qwen etc.), prepend instruction to skip thinking
        # and output JSON directly, to stay within token limits
        fallback_messages = list(messages)
        if fallback_messages and fallback_messages[-1]["role"] == "user":
            fallback_messages[-1] = {
                "role": "user",
                "content": fallback_messages[-1]["content"] + "\n\n/no_think\nIMPORTANT: Output ONLY the JSON object. Do NOT include any reasoning, thinking, or explanation. Start your response with `{`."
            }

        response = self.chat(
            messages=fallback_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=None
        )

        try:
            return self._clean_and_parse_json(response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM返回的JSON格式无效: {response[:500]}...")

