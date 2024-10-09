# import logging
# import configparser
# import os
# from ReadEmail import listen_for_new_emails
# import SendEmail
# import AskAI

# # 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # 配置文件路径
# CONFIG_FILE = 'email_config.ini'

# # 读取配置
# def read_config():
#     config = configparser.ConfigParser()
#     if not os.path.exists(CONFIG_FILE):
#         return None, None, None
#     config.read(CONFIG_FILE, encoding='utf-8')
#     return (config.get('Email', 'account', fallback=None),
#             config.get('Email', 'password', fallback=None),
#             config.get('Email', 'prompt', fallback=""))

# # 写入配置
# def write_config(account, password, prompt):
#     config = configparser.ConfigParser()
#     config['Email'] = {'account': account, 'password': password, 'prompt': prompt}
#     with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
#         config.write(configfile)

# def get_input(prompt, current=None):
#     """ 获取用户输入，如果提供了当前值，则显示当前值。 """
#     if current:
#         user_input = input(f"{prompt} (当前: {current}): ")
#         return user_input.strip() or current
#     else:
#         return input(prompt).strip()

# def change_specific_config(account, password, ai_prompt):
#     """ 提供选项让用户更改具体的配置项。 """
#     while True:
#         print("\n请选择要更改的配置项:")
#         print("1. 邮箱地址")
#         print("2. 应用授权码")
#         print("3. AI回复风格")
#         choice = input("请输入选项 (1/2/3): ").strip()

#         if choice == '1':
#             account = get_input("请输入你的QQ邮箱地址:", account)
#         elif choice == '2':
#             password = get_input("请输入你的应用授权码（不是邮箱登录密码）:", password)
#         elif choice == '3':
#             ai_prompt = get_input("你希望AI以什么风格回复邮件：\n", ai_prompt)
#         else:
#             print("无效的选项，请重新输入。")

#         # 询问用户是否继续修改
#         continue_edit = input("是否继续修改其他配置？(y/n): ").strip().lower()
#         if continue_edit != 'y':
#             break

#     return account, password, ai_prompt

# def show_and_change_config(account, password, ai_prompt):
#     """ 显示当前配置并提供更改配置的选项。 """
#     # 显示当前配置
#     print("\n当前配置:")
#     print(f"邮箱地址: {account}")
#     print(f"应用授权码: {password}")
#     print(f"AI回复风格: {ai_prompt}\n")

#     # 提供更改配置的选项
#     change_config = input("是否需要更改配置？(y/n): ").strip().lower()
#     if change_config == 'y':
#         account, password, ai_prompt = change_specific_config(account, password, ai_prompt)
#         print("修改已保存。")

#     # 保存更新后的配置
#     write_config(account, password, ai_prompt)

#     return account, password, ai_prompt

# def main():
#     # 读取上次保存的账号信息和提示
#     account, password, ai_prompt = read_config()

#     # 如果没有读取到配置文件中的数据，则从用户获取
#     if not account:
#         account = get_input("请输入你的QQ邮箱地址:")
#     if not password:
#         password = get_input("请输入你的应用授权码（不是邮箱登录密码）:")
#     if not ai_prompt:
#         ai_prompt = get_input("你希望AI以什么风格回复邮件：\n")

#     # 初始显示配置并提供更改选项
#     account, password, ai_prompt = show_and_change_config(account, password, ai_prompt)

#     # 主循环
#     try:
#         while True:
#             # 监听新邮件
#             for new_email in listen_for_new_emails(account, password):
#                 print(f"\n新邮件信息:")
#                 print(f"主题: {new_email['subject']}")
#                 print(f"发件人: {new_email['sender']}")
#                 print(f"内容: {new_email['body']}")

#                 # 生成AI回复
#                 ai_response = AskAI.askAI(new_email['subject'], new_email['sender'], new_email['body'], ai_prompt)
                
#                 # 打印发送的邮件内容
#                 print("邮件已发送:")
#                 print(f"收件人: {new_email['sender']}")
#                 print(f"主题: Re: {new_email['subject']}")
#                 print(f"内容: {ai_response}")
#                 print("---------------------------------------------")
                
#                 # 发送回复邮件
#                 SendEmail.SendMail(
#                     recipient=new_email['sender'],
#                     subject=f"Re: {new_email['subject']}",
#                     content=ai_response,
#                     sender_email=account,
#                     sender_password=password
#                 )

              

#             # 检查是否需要退出或返回修改配置
#             exit_choice = input("输入 q 退出程序，输入 c 重新显示配置，按回车继续监听: ").strip().lower()
#             if exit_choice == 'q':
#                 print("程序已退出。")
#                 break
#             elif exit_choice == 'c':
#                 account, password, ai_prompt = show_and_change_config(account, password, ai_prompt)

#     except KeyboardInterrupt:
#         print("\n邮件监听已停止。")

# if __name__ == '__main__':
#     main()


import logging
import configparser
import os
from ReadEmail import listen_for_new_emails
import SendEmail
import AskAI

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置文件路径
CONFIG_FILE = 'email_config.ini'

# 读取配置
def read_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return None, None, None
    config.read(CONFIG_FILE, encoding='utf-8')
    return (config.get('Email', 'account', fallback=None),
            config.get('Email', 'password', fallback=None),
            config.get('Email', 'prompt', fallback=""))

# 写入配置
def write_config(account, password, prompt):
    config = configparser.ConfigParser()
    config['Email'] = {'account': account, 'password': password, 'prompt': prompt}
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def get_input(prompt, current=None):
    """ 获取用户输入，如果提供了当前值，则显示当前值。 """
    if current:
        user_input = input(f"{prompt} (当前: {current}): ")
        return user_input.strip() or current
    else:
        return input(prompt).strip()

def change_specific_config(account, password, ai_prompt):
    """ 提供选项让用户更改具体的配置项。 """
    while True:
        print("\n请选择要更改的配置项:")
        print("1. 邮箱地址")
        print("2. 应用授权码")
        print("3. AI回复风格")
        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == '1':
            account = get_input("请输入你的QQ邮箱地址:", account)
        elif choice == '2':
            password = get_input("请输入你的应用授权码（不是邮箱登录密码）:", password)
        elif choice == '3':
            ai_prompt = get_input("你希望AI以什么风格回复邮件：\n", ai_prompt)
        else:
            print("无效的选项，请重新输入。")

        # 询问用户是否继续修改
        continue_edit = input("是否继续修改其他配置？(y/n): ").strip().lower()
        if continue_edit != 'y':
            break

    return account, password, ai_prompt

def show_and_change_config(account, password, ai_prompt):
    """ 显示当前配置并提供更改配置的选项。 """
    # 显示当前配置
    print("\n当前配置:")
    print(f"邮箱地址: {account}")
    print(f"应用授权码: {password}")
    print(f"AI回复风格: {ai_prompt}\n")

    # 提供更改配置的选项
    change_config = input("是否需要更改配置？(y/n): ").strip().lower()
    if change_config == 'y':
        account, password, ai_prompt = change_specific_config(account, password, ai_prompt)
        print("修改已保存。")

    # 保存更新后的配置
    write_config(account, password, ai_prompt)

    return account, password, ai_prompt

def main():
    # 读取上次保存的账号信息和提示
    account, password, ai_prompt = read_config()

    # 如果没有读取到配置文件中的数据，则从用户获取
    if not account:
        account = get_input("请输入你的QQ邮箱地址:")
    if not password:
        password = get_input("请输入QQ邮箱授权码（IMAP/SMTP服务）:")
    if not ai_prompt:
        ai_prompt = get_input("AI的风格及对其要求：\n")

    # 初始显示配置并提供更改选项
    account, password, ai_prompt = show_and_change_config(account, password, ai_prompt)

    # 主循环
    try:
        while True:
            # 监听新邮件
            for new_email in listen_for_new_emails(account, password):
                try:
                    print(f"\n新邮件信息:")
                    print(f"主题: {new_email['subject']}")
                    print(f"发件人: {new_email['sender']}")
                    print(f"内容: {new_email['body']}")

                    # 生成AI回复
                    ai_response = AskAI.askAI(new_email['subject'], new_email['sender'], new_email['body'], ai_prompt)
                    
                    # 打印发送的邮件内容
                    print("邮件已发送:")
                    print(f"收件人: {new_email['sender']}")
                    print(f"主题: Re: {new_email['subject']}")
                    print(f"内容: {ai_response}")
                    print("------------------------------------------------------------------------")
                    
                    # 发送回复邮件
                    SendEmail.SendMail(
                        recipient=new_email['sender'],
                        subject=f"Re: {new_email['subject']}",
                        content=ai_response,
                        sender_email=account,
                        sender_password=password
                    )
                except Exception as e:
                    pass

            # 检查是否需要退出或返回修改配置
            exit_choice = input("输入 q 退出程序，输入 c 重新显示配置，按回车继续监听: ").strip().lower()
            if exit_choice == 'q':
                print("程序已退出。")
                break
            elif exit_choice == 'c':
                account, password, ai_prompt = show_and_change_config(account, password, ai_prompt)

    except KeyboardInterrupt:
        print("\n邮件监听已停止。")
    except Exception as e:
        pass

if __name__ == '__main__':
    main()