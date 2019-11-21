# coding: utf-8
import discord
import requests
import json
import re
import random

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
                #それっぽくなるように整形
                #「な、ニャ」および文末の「ぜ、わ、よ、ｗ」を「にゃ」に変換、文末の「笑」を削除
                res_text = re.sub("[ぜわよ|ね？|か?|w]$","にゃ",str(res['result']).replace('ニャ', 'にゃ').rstrip("笑"))
                if re.compile(".*にゃ$").search(res_text):
                    pass
                else:
                    res_text = res_text.replace('な', 'にゃ')
                #「？」で終わる文以外は、文末に「☆、～♪、～、！」をのいずれか1つををランダムに追加
                gobi = ["☆","～♪","～","！","",""]
                if '?' in res_text or '？' in res_text or '！' in res_text: 
                    m = str(res_text)
                else:
                    m = str(res_text) + str(random.choice(gobi))
                await message.channel.send(m)

client.run(token)
