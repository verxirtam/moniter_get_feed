#! /usr/bin/python3
# -*- coding: utf-8 -*-

#パッケージのインポート
#メール送受信に使用
import smtplib
from email.mime.text import MIMEText
#プロセス監視に使用
import subprocess
#コマンドライン引数に使用
import sys

#監視するプロセス名
process_name = "/bin/bash ./get_feed.sh"

#メール情報ファイル
mail_info_path = "../conf/moniter_mail_info.txt"

#プロセス起動中のメッセージ
run_title = "[info] get_feed.sh status"
run_body  = "get_feed.sh is running."

#プロセス停止中のメッセージ
not_run_title = "[error] get_feed.sh status"
not_run_body  = "get_feed.sh is not running."

#プロセスの有無を確認して
#プロセスがあればTrue、そうでなければFalseを返す
def is_running(psname):
    command_string = 'ps -aux | grep "' + psname + '" | grep -v grep > /dev/null'
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

def send_info_mail(mail_title, mail_body):
    mail_info = {}
    get_mail_info(mail_info)
    mail_info["title"] = mail_title
    mail_info["body"] = mail_body
    send_mail(mail_info)


######################################################################################

if __name__ == '__main__':
    #監視対象のプロセス起動時にメール送信するかどうかを切り替えられるようにする
    #起動していない場合はオプションによらずメール送信する
    
    #コマンドライン引数を取得
    args = sys.argv
    argc = len(args)
    
    #Trueの場合、問題ない場合はメール送付しない
    send_if_ok = False
    if argc == 2 and args[1]=="-s":
        send_if_ok = True
    
    
    #プロセスが起動しているかチェック
    if is_running(process_name):
        #起動している場合
        if send_if_ok:
            send_info_mail(run_title, run_body)
    else:
        #起動していない場合
        send_info_mail(not_run_title, not_run_body)





######################################################################################
