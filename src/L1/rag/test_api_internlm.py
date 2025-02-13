from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
api_key = os.getenv("internlm_api_key")
model="internlm2.5-latest"

client = OpenAI(
    api_key=api_key , 
    base_url=base_url,
)

chat_rsp = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "xtuner是什么？"}],
)

for choice in chat_rsp.choices:
    print(choice.message.content)