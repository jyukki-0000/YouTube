from googleapiclient.discovery import build
import csv
import isodate

# YouTube Data APIキーを設定します
DEVELOPER_KEY = "YOUR_DEVELOPER_KEY"

# YouTube APIのバージョンとサービス名を設定します
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# 指定したチャンネルIDの最新の動画情報を取得する関数
def get_channel_videos(channel_id):
    # YouTube APIクライアントを作成します
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # 指定したチャンネルIDの最新の動画を検索します
    search_response = youtube.search().list(
        channelId=channel_id,
        part="id,snippet",
        maxResults=50,
        order="date"
    ).execute()

    # 検索結果から動画情報を取得します
    videos = []
    for search_result in search_response.get("items", []):
        if search_result['snippet']['liveBroadcastContent'] == 'none':
            videos.append({
                'タイトル': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            })

    # アップロードされた動画が10個以上得られるまで検索を続けます
    while len(videos) < 10:
        nextPageToken = search_response.get('nextPageToken')
        if not nextPageToken:
            break
        search_response = youtube.search().list(
            channelId=channel_id,
            part="id,snippet",
            maxResults=50,
            order="date",
            pageToken=nextPageToken
        ).execute()
        for search_result in search_response.get("items", []):
            if search_result['snippet']['liveBroadcastContent'] == 'none':
                videos.append({
                    'タイトル': search_result['snippet']['title'],
                    'videoId': search_result['id']['videoId']
                })

    # アップロードされた動画が10個以上ある場合は、最新の10個だけを取得します
    videos = videos[:10]

    # 各動画の詳細情報を取得します
    for video in videos:
        video_response = youtube.videos().list(
            part='statistics,contentDetails',
            id=video['videoId']
        ).execute()

        # 動画の再生回数、高評価数、動画時間を取得します
        video['再生回数'] = video_response['items'][0]['statistics'].get('viewCount', 'N/A')
        video['高評価数'] = video_response['items'][0]['statistics'].get('likeCount', 'N/A')
        duration = isodate.parse_duration(video_response['items'][0]['contentDetails']['duration'])
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        video['動画時間'] = f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"

    # 動画情報のリストを返します
    return videos

# 動画情報をCSV形式で保存する関数
def save_as_csv(videos, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['タイトル', '再生回数', '高評価数', '動画時間']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # ヘッダー行を書き込みます
        writer.writeheader()

        # 各動画の情報を行として書き込みます
        for video in videos:
            writer.writerow({
                'タイトル': video['タイトル'],
                '再生回数': video['再生回数'],
                '高評価数': video['高評価数'],
                '動画時間': video['動画時間']
            })

# チャンネルIDを指定して動画情報を取得します
videos = get_channel_videos("YOUR_CHANNEL_ID")

# 動画情報をCSV形式で保存します
save_as_csv(videos, 'videos.csv')