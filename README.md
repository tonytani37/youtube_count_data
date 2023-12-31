## youtubeの動画再生回数を取得してJSONファイルでログとして記録する

APIを使って取得したyoutubeの指定動画の再生回数等情報を、jsonファイルとしてログに残す処理です。

Github Actionsを使い、Pythonで書いたスクリプトで収集したデータをjsonファイルにし、
gitコマンドでレジストリのrootにpushする一連の処理を実行

ポイントは

１．Github Actionsでpythonがファイルを出力したrootはあくまで実行環境内でのrootのため、Actionsの実行が完了すると消えてしまう。

２．そのためpythonスクリプトの実行直後にgitでリポジトリへpushする必要がある。

３．pushされるレジストリは、Actionsを動かした（ymlファイルが登録されている）レジストりのこと。

４．pushされたファイルはレジストリのrootに置かれる。（パス指定すれば良いかもしれないけどやってない）


## 公開レジストリで使う秘密情報の扱い方
settingのsecrets and variablesのActions secrets and variablesのsecretsに
youtube api用のキー情報を登録すれば、ソースを見てもキーは見えない。

その場合、ymlファイルとpythonスクリプトには以下のように記述すること。

Actions secrets and variablesのsecretsで指定した名前

　youtube_key

ymlファイル内の記述
```
env:
  youtube_key : ${{ secrets.youtube_key }}
```
　${{ secrets.youtube_key }}で指定している「youtube_key」　は、リポジトリの　secrets　で指定した名前

pythonのキー情報取得の記述
```
api_key = os.environ['youtube_key']
```
os.environ['youtube_key']で指定している「youtube_key」　は、ymlで参照した名前のセットした変数名
