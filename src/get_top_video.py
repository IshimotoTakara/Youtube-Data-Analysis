'''
急上昇動画を${video_num}件取得して、json形式で保存するプログラム

'''
import googleapiclient.discovery  # pip install google-api-python-client
import json
import os
import sys

def main(top_video_dir, video_num, api_key):
    os.makedirs(top_video_dir, exist_ok=True)
    json_file_path = top_video_dir + f"/youtubetop{video_num}.json"

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular", # 急上昇
        maxResults=video_num,  # ここで個数を指定する
        regionCode="JP"  # ここで場所(国)の指定
    )

    # 辞書型をjsonに変換して保存
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(request.execute(), f, indent="\t", ensure_ascii=False)

if __name__ == '__main__':
    top_video_dir = sys.argv[1]
    video_num = sys.argv[2]
    api_key = sys.argv[3]
    
    main(top_video_dir, video_num, api_key)
