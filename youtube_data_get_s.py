import googleapiclient.discovery
from datetime import datetime, timedelta, timezone
import json
import requests
import os

# search_responseからはvideo_idを取得しているので、手動でvideo_idを取得してリストを作ること。
# キーワードだけでは全てのvideo_idは取得できなかったため手で調べてリストを作った（データ取得できてもいろいろ混ざってしまう）

# dataを取得するタイミングで並び順はバラバラっぽいので、ここで固定したことにする。合わせて識別名としてメンバーの名前をvalueにしたdictに変更

# jsonのフォーマット説明
# {採取日付:{'date':採取日付,'values':[{'videoID' : i ,'name':名前, 'title': 動画タイトル, 'view': 再生回数, 'like' : いいね数 , 'comment' : コメント数} .... ]}}
# valuesの要素はリストで、その要素は採取されたメンバー分それぞれのデータがdict形式

members = {
            # "4s0p8CLINZE" : '池田',
            # "5yKq5iQWh8w" : '小川',
            # "iPRx9OWYQ64" : '一ノ瀬',
            # "Jrr5Efd5VZQ" : '井上',
            # "Ou5wLI7nFVY" : '菅原',
            # "pIEPFMOjQQ4" : '川﨑',
            # "sWjdK1EEgG4" : '中西',
            # "tFPBGAGQeq0" : '富里',
            # "w2-5lxXST9g" : '奥田',
            "x_BjvhMW9TE" : '承認欲求'
            }

# APIキーを設定
api_key = os.environ['youtube_key']


def Youtube_Data_Set(yymmdd):
# YouTube Data APIのリソースを取得
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    kekka = [youtube.videos().list(
                part='snippet,statistics',
                id=search_id
                    ).execute() for search_id in members]

    pv_01=[[n['items'][0]['snippet']['title'],int(n['items'][0]['statistics']['viewCount']),int(n['items'][0]['statistics']['likeCount']),int(n['items'][0]['statistics']['commentCount'])] for n in kekka]

    nogi = [{'videoID' : i ,'name':members[i], 'title': n[0], 'view':  n[1], 'like' : n[2] , 'comment' : n[3]} for n , i in zip(pv_01,members)]

    json_data = { "date" : yymmdd , "values" : nogi }

    return json_data


# 日付をプライマリーにしているので、同じ日付ならばあとから採取されたデータが常に上書きされる
# 結果、間違って同じ日に何度も実行されても、最新のデータのみ残る（これがいいかどうかわからんけど）

# def Youtube_Log():
#　日付は日本時間にセットし直しています
yymmdd = datetime.now(timezone(timedelta(hours=+9))).strftime('%Y-%m-%d %H:%M:%S')
# yymmdd = "2023-09-23" # テスト用に日付を強制設定してる
data = Youtube_Data_Set(yymmdd) # Youtubeからデータを引っ張ってきてjsonフォーマットに整形する

if os.path.exists('./sakura.json'): # ファイルが存在する場合にはそいつを読み込んで日付キーで要素を追加する
            try:
                        with open('./sakura.json', 'r') as f:
                            log_json = json.load(f)
                        log_json[yymmdd] = data
            except Exception as e:
                        print(e)
else:
            log_json = { yymmdd : data } # ファイルが無いときには新規で作る

try:
            with open('./sakura.json','w') as f:
                        json.dump(log_json,f)
except FileNotFoundError:
    print("指定したファイルが見つかりません。")
except PermissionError:
    print("ファイルを開くための適切な権限がありません。")
except Exception as e:
    print(f"エラーが発生しました: {str(e)}")
