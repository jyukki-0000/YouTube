# YouTube Channel Video Info Scraper

このプロジェクトは、指定したYouTubeチャンネルの最新の動画（生放送を除く）10個について、そのタイトル、再生回数、高評価数、動画時間を取得し、CSV形式で出力するPythonスクリプトです。

## 使い方

1. このリポジトリをクローンまたはダウンロードします。

2. スクリプト（`main.py`など）の中の`YOUR_DEVELOPER_KEY`をあなたのYouTube Data APIキーに置き換えます。

3. 同じくスクリプトの中の`YOUR_CHANNEL_ID`を取得したい動画のあるチャンネルのIDに置き換えます。

4. スクリプトを実行します。例えば、コマンドラインでは次のように実行します：

5. `videos.csv`という名前のCSVファイルが出力されます。このファイルには、各動画のタイトル、再生回数、高評価数、動画時間が含まれます。

## 必要なライブラリ

このスクリプトを実行するには、以下のPythonライブラリが必要です：

- google-api-python-client
- isodate

これらのライブラリは、次のコマンドでインストールできます：
pip install --upgrade google-api-python-client isodate

## 注意

YouTube Data APIの使用にはクォータ制限があります。一定のリクエスト数を超えると追加の料金が発生する可能性があります。詳細は[YouTube Data APIのドキュメンテーション](https://developers.google.com/youtube/v3/determine_quota_cost)を参照してください。
