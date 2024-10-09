import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def SendMail(recipient, subject, content, sender_email, sender_password):
    """
    发送邮件
    :param recipient: 收件人邮箱地址
    :param subject: 邮件主题
    :param content: 邮件内容
    :param sender_email: 发件人邮箱地址
    :param sender_password: 发件人邮箱密码或应用专用密码
    """
    # 创建MIMEMultipart对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = Header(subject, 'utf-8')

    # 添加邮件正文
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

   
    # 连接到SMTP服务器
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        # 登录
        server.login(sender_email, sender_password)

        # 发送邮件
        logging.info(f"发送邮件给 {recipient}...")
        server.sendmail(sender_email, recipient, msg.as_string())
        logging.info("邮件发送成功！")

# 示例调用
# if __name__ == "__main__":
#     recipient = "recipient@example.com"
#     subject = "测试邮件"
#     content = "这是一封测试邮件。"
#     sender_email = "your-email@qq.com"
#     sender_password = "your-app-password"

#     SendMail(recipient, subject, content, sender_email, sender_password)