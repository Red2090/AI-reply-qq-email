import logging
from openai import OpenAI
import main


def askAI(subject, sender, body, ai_prompt):
    client = OpenAI(api_key="", base_url="")
    '''
    add your own api and api key here
    '''
    
    response = client.chat.completions.create(
        model="",  # your own model name 
        messages=[
            {"role": "system", "content": "You are a email response assistant"},
            {"role": "user", "content": f"你现在是一个以下风格的ai：{ai_prompt}。以下有一封邮件，主题是 {subject}，发件人是 {sender}，邮件内容是{body}，请帮我回复邮件，发挥想象力。"},
        ],
        stream=False
    )
    
    aiResponse = response.choices[0].message.content
    return aiResponse

