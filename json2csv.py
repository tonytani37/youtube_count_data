import json
import requests
import pandas as pd

# url = 'https://raw.githubusercontent.com/tonytani37/youtube_count_data/main/nogi.json'

# jdata = json.loads(requests.get(url).text)

with open('./nogi.json') as f:
    jdata = json.load(f)

fm = "2023-09-01"
# to = "2023-09-30"
to = "9999-99-99"

d = [a for a in jdata if (a >= fm and a <= to)]

counts = [
            ['池田'],
            ['小川'],
            ['一ノ瀬'],
            ['井上'],
            ['菅原'],
            ['川﨑'],
            ['中西'],
            ['富里'],
            ['奥田'],
            ['五百城']
        ]



for z in jdata.values():
    for dd in d:
        if z['date'] == dd:
            for i,x in enumerate(z['values']):
                counts[i].append(x['view'])

# countsをDataFrameにして整形してからcsvファイルに出力する

clms = ['name']
for dt in d:
    clms.append(dt)

df = pd.DataFrame(counts,columns=clms)

df.set_index('name').to_csv('nogi.csv')
