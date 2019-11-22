# coding: utf-8
import discord
import requests
import json
import re
import random

"""
ユーザーローカル社のチャットボットAPIを用いたネコ風ボット
https://ai.userlocal.jp/document/free/top/
上記リンクからAPIキーを申請してください。
"""

client = discord.Client()

token = "discordbotのトークンを入れてね"
key = "APIのキーを入れてね"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # 「>」で始まるか調べる
    if message.content.startswith(">"):
        # メッセージの送り主Bot以外だった場合のみ反応
        if client.user != message.author:
            # サーバ側から終了できないので必須
            if message.content == '>お疲れさま' or message.content == '>お疲れにゃ':
                await message.channel.send('お疲れさまにゃ♪')
                print('ログアウトしました')
                await client.logout()
            else:
                # メッセージを書きます
                #自動会話APIにメッセージを送信
                url = "https://chatbot-api.userlocal.jp/api/chat?message=" + message.content + "&key=" + key
                res = requests.get(url).json()
                #帰ってきたメッセージをキャラクター会話変換APIでネコ語に変換
                url = "https://chatbot-api.userlocal.jp/api/character?message=" + str(res['result']) + "&key=" + key + "&character_type=cat"
                res = requests.get(url).json()
                await message.channel.send(res['result'])

client.run(token)
