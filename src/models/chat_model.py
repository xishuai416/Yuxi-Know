import os
from openai import OpenAI
from utils.logging_config import setup_logger


logger = setup_logger(__name__)

class OpenAIBase():
    def __init__(self, api_key, base_url, model_name):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def predict(self, message, stream=False):

        logger.debug(message)
        if isinstance(message, str):
            messages=[{"role": "user", "content": message}]
        else:
            messages = message

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=stream,
        )
        logger.debug(response)

        if stream:
            return self._stream_response(messages)
        else:
            return self._get_response(messages)

    def _stream_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True,
        )
        for chunk in response:
            yield chunk.choices[0].delta

    def _get_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message


class DeepSeek(OpenAIBase):
    def __init__(self, model_name=None):
        model_name = model_name or "deepseek-chat"
        api_key = os.getenv("DEEPSEEKAPI")
        base_url = "https://api.deepseek.com"
        super().__init__(api_key=api_key, base_url=base_url, model_name=model_name)


class Zhipu(OpenAIBase):
    def __init__(self, model_name=None):
        model_name = model_name or "glm-4"
        api_key = os.getenv("ZHIPUAPI")
        base_url = "https://open.bigmodel.cn/api/paas/v4/"
        super().__init__(api_key=api_key, base_url=base_url, model_name=model_name)