#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, re, os
from os.path import realpath

root = "./"

def flatten(path):
        canonical = "/".join([root, realpath(path)])
        relative_path = canonical.replace(root + "/", "")
        return relative_path

def fread(path):
        # ファイルが存在しない場合にNone返し
        # ディレクトリならば $(ls -l) コマンド
        # ファイルならば中身を読み込み返す
        if not os.path.exists(path):
                return None
        if os.path.isdir(path):
                return "$(ls -l)".encode("utf-8")
        with open(path, "rb") as f:
                data = f.read()
        return data

def parse(string, path):
        # 文字列内コマンド形式をそのコマンドの結果に代入し、
        # リンクに<a>タグを追加する。
        links = re.compile(r'^(https://.*)$', flags=re.MULTILINE)
        commands = re.compile(r'\$\((.*?)\)', flags=re.MULTILINE)
        string = string.replace("$root", root + "/content")
        for command in commands.findall(string):
                string = string.replace("$(%s)" % command, run(command, path))
        for link in links.findall(string):
                string = string.replace("%s" % link, "<a target='_blank' href='{0}'>{0}</a>".format(link))
        string = string.replace("\\$", "$").replace("\\\\", "\\")
        return string

def run(command, path):
        # パスからファイル名を省く
        if not os.path.isdir(path):
                path = "/".join(path.split("/")[:-1])
        command = "cd %s; %s" % (path, command)
        output = subprocess.check_output(command, shell=True).decode("utf-8")

        command = command.split(" ")[2:]
        # print("[* run] Command: %s" % command)
        if command[0] == "ls" and command[1] == "-l":
                output = output.split("\n")
                output2 = ""
                for line in [line.split(" ") for line in output]:
                        if len(line) >= 10:
                                file = line[-1]
                                directory = line[0][0] == "d"
                                hyperlink = "<a href='{0}{1}'>{0}</a>".format(
                                        file,
                                        "/" if directory else ""
                                )
                                line[-1] = hyperlink
                                # print("[* run] Line: %s" % line)
                        output2 += " ".join(line) + "\n"
                output = output2[:-1]
        return output
