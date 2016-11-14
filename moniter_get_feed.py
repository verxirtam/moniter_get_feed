#! /usr/bin/python3
# -*- coding: utf-8 -*-

#パッケージのインポート
#メール送受信に使用
import smtplib
from email.mime.text import MIMEText
#プロセス監視に使用
import subprocess


#監視するプロセス名
process_name = "/bin/bash ./get_feed.sh"

#メール情報ファイル
mail_info_path = "../conf/moniter_mail_info.txt"


#プロセスの有無を確認して
#プロセスがあればTrue、そうでなければFalseを返す
def is_running(psname):
    command_string = 'ps -aux | grep "' + psname + '" | grep -v grep'
    ret = subprocess.call(command_string, shell = True)
    if ret == 0:
        return True
    else:
        return False


#メール関連の情報取得
def get_mail_info(mail_info):
    #メール情報ファイルオープン
    mail_info_file = open(mail_info_path)
    #送信元アドレス取得
    mail_info["from"]     = mail_info_file.readline()
    print("mail[\"from\"] : " + mail_info["from"])
    #送信元パスワード取得
    mail_info["password"] = mail_info_file.readline()
    #送信先アドレス取得
    mail_info["to"]       = mail_info_file.readline()
    #ファイルクローズ
    mail_info_file.close()

#メールの送信
def send_mail(mail_info):
    #MIMEオブジェクトの作成
    msg = MIMEText(mail_info["body"])
    msg['Subject'] = mail_info["title"]
    msg['From'] = mail_info["from"]
    msg['To'] = mail_info["to"]
    #SMTP認証し送信
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(mail_info["from"], mail_info["password"])
    s.send_message(msg)
    s.close()


######################################################################################

if __name__ == '__main__':
    #TODO コマンドラインオプションに対応する
    #監視対象のプロセス起動時にメール送信するかどうかを切り替えられるようにする
    #起動していない場合はオプションによらずメール送信する
    
    #プロセスが起動しているかチェック
    if is_running(process_name):
        #起動している場合
        #TODO titleとbodyだけ渡してメール送付できるように関数を定義する
        #TODO titleとbodyの内容はグローバルスコープで定義する
        mail_info = {}
        get_mail_info(mail_info)
        mail_info["title"] = "[info] get_feed.sh status"
        mail_info["body"] = "get_feed.sh is running."
        send_mail(mail_info)
    else:
        #起動していない場合
        mail_info = {}
        get_mail_info(mail_info)
        mail_info["title"] = "[error] get_feed.sh status"
        mail_info["body"] = "get_feed.sh is not running."
        send_mail(mail_info)





######################################################################################
