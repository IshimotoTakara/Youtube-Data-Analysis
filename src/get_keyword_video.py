'''
${keyword}を含むタイトルの動画を再生回数順で取得して、json形式で保存する。

'''
import googleapiclient  # pip install google-api-python-client
import json
import os
import sys

def main(keyword_video_dir, keyword, api_key):
    os.makedirs(keyword_video_dir, exist_ok=True)
    json_file_path = keyword_video_dir + f"/youtubetop_{keyword}.json"

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part='snippet',  # 取得情報
        q=keyword,  # 検索したい文字列を指定
        order='viewCount',  # 視聴回数が多い順に取得
        type='video',
    ).execute()

    # 辞書型をjsonに変換して保存
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(request.execute(), f, indent="\t", ensure_ascii=False)


if __name__ == '__main__':
    keyword_video_dir = sys.argv[1]
    keyword = sys.argv[2]
    api_key = sys.argv[3]

    main(keyword_video_dir, keyword, api_key)
