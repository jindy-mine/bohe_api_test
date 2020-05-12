"""
=========================================
Author:薄咊
Time:2020/4/13  23:22
comments:Study_day01
==========================================
"""
import smtplib,os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from common.handle_path import REPORT_DIR

def send_msg():
    user = "jindi_han@qq.com"
    password = "fvbtpvkrvyqijjfe"
    # 第一步：连接smtp服务器，并登录
    # 连接到smtp服务器
    smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
    # 登录smtp服务器（使用邮箱账号和授权码进行登录）
    smtp.login(user=user, password=password)

    # 第二步：构造一封多组件邮件
    msg = MIMEMultipart()
    # 邮件主题
    msg["Subject"]="上课邮件001"
    # 收件人(显示的收件人)
    msg["To"]=user
    # 发件人（显示的发件人）
    msg["From"]=user

    # 构建邮件的文本内容
    text = MIMEText("邮件中的文本内容",_charset="utf8")
    msg.attach(text)

    # 构造邮件的附件
    # 读取文件内容，作为正文发送：邮件显示不友好
    with open(os.path.join(REPORT_DIR,"ApiReport.html"),"rb") as f:
        content = f.read()
    report = MIMEApplication(content)
    report.add_header('content-disposition', 'attachment', filename='python.html')
    msg.attach(report)

    # 第三步：发送邮件(邮件内容，发件人地址-实际发件人邮箱，收件人地址-实际收件人邮箱)
    smtp.send_message(msg,from_addr=user,to_addrs=user)