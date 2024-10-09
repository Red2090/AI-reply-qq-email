import logging
from openai import OpenAI
import main


def askAI(subject, sender, body, ai_prompt):
    client = OpenAI(api_key="sk-be5f4a8e6cab409098bea385f4421ad0", base_url="https://api.deepseek.com")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a email response assistant"},
            {"role": "user", "content": f"你现在是一个以下风格的ai：{ai_prompt}。以下有一封邮件，主题是 {subject}，发件人是 {sender}，邮件内容是{body}，请帮我回复邮件，发挥想象力。"},
        ],
        stream=False
    )
    
    aiResponse = response.choices[0].message.content
    return aiResponse


# if __name__ == "__main__":
#     subject = "关于项目进度"
#     sender = "张三 <zhangsan@example.com>"
#     body = "你好，我想知道项目的当前进度。谢谢！"
#     reply = askAI(subject, sender, body)
#     print(reply)

