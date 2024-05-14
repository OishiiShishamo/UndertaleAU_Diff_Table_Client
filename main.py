import pandas as pd
from pathlib import Path
import os
import shutil
import git
import atexit
import sys

#table_list = pd.read_csv("./list.csv")

#ログ表示用

def log_text(log_text):
    print("[log] " + str(log_text))

#難易度表のディレクトリー名用
#Table Directory Formatの略

def tdf(table_name, table_auther):
    return "[" + table_auther + "] " + table_name

#ただのヘルプ表示用関数
#名前の通り

def help():
    print("help or man:ヘルプを閲覧")
    print("update:list.csvに記載されている難易度表をダウンロードorアップデートする")
    print("list:難易度表リストを確認する")
    print("view:難易度表を閲覧する")
    print("exit:このアプリケーションを終了する")

#難易度表アップデート用

def table_update(table_list):
    #log_text(str(table_list.shape[0]) + "行存在")
    for i in range(table_list.shape[0]):
        print(tdf(table_list.iloc[i, 0], table_list.iloc[i, 1]))
        if os.path.isdir("./[" + table_list.iloc[i, 1] + "] " + table_list.iloc[i, 0]) == False:
            git.Repo.clone_from("https://github.com/" + table_list.iloc[i, 1] + "/" + table_list.iloc[i,0] + ".git", tdf(table_list.iloc[i, 0], table_list.iloc[i, 1]))
            log_text("Clone")
        else:
            repo = git.Repo("./" + tdf(table_list.iloc[i, 0], table_list.iloc[i, 1]))
            origin = repo.remotes.origin
            origin.pull()
            log_text("Pull")

#難易度表リストを表示する

def view_list(table_list):
    for i in range(table_list.shape[0]):
        print(str(i) + "." + str(tdf(table_list.iloc[i, 0], table_list.iloc[i, 1])))

#難易度表の中身を表示する

def view_table(table_list):
    for i in range(table_list.shape[0]):
        print(str(i) + "." + str(tdf(table_list.iloc[i, 0], table_list.iloc[i, 1])))
    print("表示する難易度表を選択してください(半角数字)>", end="")
    table_num = input()
    if(int(table_num) < int(table_list.shape[0])):
        table = pd.read_csv("./" + tdf(table_list.iloc[int(table_num), 0], table_list.iloc[int(table_num), 1]) + "/data.csv")
        for i in range(table.iloc[0, 1], table.iloc[0, 2] + 1, 1):
            print(str(table.iloc[0, 0]) + str(i))
        print("表示する難易度を選択してください(半角数字)>", end="")
        num = int(input())
        if(int(table.iloc[0, 1]) < num):
            if(int(table.iloc[0, 2]) > num):
                diff = pd.read_csv("./" + tdf(table_list.iloc[int(table_num), 0], table_list.iloc[int(table_num), 1]) + "/" + str(num) + ".csv")
                for i in range(diff.shape[0]):
                    print(str(i) + "." + str(diff.iloc[i, 0]) + ":" + str(diff.iloc[i, 1]))
            else:
                print("存在しない難易度を指定しています。")
        else:
            print("存在しない難易度を指定しています。")
    else:
        print("存在しない難易度表を指定しています。")

#何をするかを聞く
#無限ループする

def question():
    while(1):
        print(">", end="")
        i = input().strip()
        match(i):
            case i if i == "help" or i == "man":
                help()
            case i if i == "update":
                table_update(pd.read_csv("./list.csv"))
            case i if i == "list":
                table_update(pd.read_csv("./list.csv"))
                view_list(pd.read_csv("./list.csv"))
            case i if i == "view":
                table_update(pd.read_csv("./list.csv"))
                view_table(pd.read_csv("./list.csv"))
            case i if i == "exit":
                sys.exit()

#main関数
#それ以上でもそれ以下でもない

def main():
    print("UndertaleAU Diff Table Client ver 0.01")
    print("helpかmanでヘルプを見れる")
    question()

#main関数を実行してるだけ

main()