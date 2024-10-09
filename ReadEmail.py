import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# QQ邮箱IMAP服务器地址
IMAP_SERVER = 'imap.qq.com'

def get_decoded_header(header, extract_email=False):
    """
    解码邮件头部信息
    :param header: 邮件头部
    :param extract_email: 如果为True，则仅提取邮箱地址
    :return: 解码后的头部信息或邮箱地址
    """
    logging.debug(f"解码头部: {header}")
    decoded_bytes, encoding = decode_header(header)[0]
    if isinstance(decoded_bytes, bytes):
        decoded_str = decoded_bytes.decode(encoding or 'utf-8')
    else:
        decoded_str = decoded_bytes

    if extract_email:
        # 使用email.utils.parseaddr来提取邮箱地址
        _, addr = parseaddr(decoded_str)
        return addr  # 返回邮箱地址
    return decoded_str

def decode_payload(payload, charset=None):
    """
    解码邮件内容
    :param payload: 邮件内容
    :param charset: 编码方式
    :return: 解码后的邮件内容
    """
    logging.debug(f"尝试解码内容，使用字符集: {charset}")
    if charset:
        try:
            return payload.decode(charset)
        except UnicodeDecodeError:
            pass  # 如果指定的编码失败，继续尝试其他编码

    # 尝试多种常见的编码方式
    for encoding in ['utf-8', 'gb2312', 'gbk', 'iso-8859-1', 'latin1']:
        try:
            logging.debug(f"尝试使用编码: {encoding}")
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue

    # 如果所有编码都失败，返回原始字节
    logging.warning("所有编码尝试失败，使用替换字符解码")
    return payload.decode('utf-8', errors='replace')

def process_new_emails(mail, last_message_count):
    """
    处理新邮件
    :param mail: IMAP4_SSL 对象
    :param last_message_count: 上次检查时的消息数量
    :return: 新邮件的信息列表和最新的消息数量
    """
    status, messages = mail.search(None, 'ALL')
    message_ids = messages[0].split()
    new_message_count = len(message_ids)

    if new_message_count > last_message_count:
        new_messages = message_ids[last_message_count:]
        new_emails = []

        for msg_id in new_messages:
            logging.info(f"处理新邮件ID: {msg_id}")
            # 获取邮件数据
            status, data = mail.fetch(msg_id, '(RFC822)')
            raw_email = data[0][1]

            # 解析邮件
            msg = email.message_from_bytes(raw_email)

            # 提取邮件主题
            subject = get_decoded_header(msg['Subject'])
            logging.info(f"提取邮件主题: {subject}")

            # 提取发件人邮箱
            sender = get_decoded_header(msg['From'], extract_email=True)
            logging.info(f"提取发件人邮箱: {sender}")

            # 遍历邮件部分以获取正文
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # 跳过附件
                    if "attachment" not in content_disposition:
                        if content_type == 'text/plain':
                            charset = part.get_content_charset()  # 获取邮件内容的字符集
                            body += decode_payload(part.get_payload(decode=True), charset)
            else:
                # 如果邮件不是多部分的，则直接读取正文
                charset = msg.get_content_charset()
                body = decode_payload(msg.get_payload(decode=True), charset)

            # 添加新邮件信息到列表
            new_emails.append({
                'subject': subject,
                'sender': sender,
                'body': body
            })

        return new_emails, new_message_count
    else:
        return [], last_message_count

def listen_for_new_emails(email_account, app_password):
    """
    开始监听新邮件
    :param email_account: 邮箱账号
    :param app_password: 应用专用密码
    """

    # 初始化IMAP4_SSL对象
    logging.info("初始化IMAP4_SSL对象...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    try:
        logging.info("尝试连接到IMAP服务器...")
        # 登录
        mail.login(email_account, app_password)
        logging.info("登录成功")

        # 选择收件箱
        mail.select('inbox')

        # 获取初始邮件数量
        status, messages = mail.search(None, 'ALL')
        last_message_count = len(messages[0].split())
        
        logging.info("正在监测新邮件...")
        
        while True:
            # 检查是否有新邮件 
            new_emails, last_message_count = process_new_emails(mail, last_message_count)

            for new_email in new_emails:
                yield new_email  # 使用生成器返回每封新邮件

            # 等待一段时间后再次检查
            time.sleep(10) 
    except KeyboardInterrupt:
        logging.info("监听中断，退出...")
    except Exception as e:
        logging.error(f"发生错误: {e}", exc_info=True)
    finally:
        # 关闭连接
        logging.info("关闭IMAP连接...")
        mail.logout()

# 示例调用
# if __name__ == "__main__":
#     email_account = "your-email@qq.com"
#     app_password = "your-app-password"
    
#     for new_email in listen_for_new_emails(email_account, app_password):
#         print(new_email)