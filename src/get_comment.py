'''
${video_ids}内のそれぞれのビデオIDに対応する動画のコメントをCSVファイルに保存する。

'''
import requests
import urllib.parse as parse
import csv
import json
import os
import sys


def get_comment(video_id, exe_num, api_key):
    URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
    nextPageToken = ''
    item_count = 0
    items_output = [
                # ['videoId']+
                ['textDisplay'] +
                ['textOriginal'] +
                ['authorDisplayName'] +
                # ['authorProfileImageUrl']+
                # ['authorChannelUrl']+
                # ['authorChannelId']+
                # ['canRate']+
                # ['viewerRating']+
                ['likeCount'] +
                ['publishedAt'] +
                ['updatedAt']
    ]

    for i in range(exe_num):
            #APIパラメータセット
            param = {
                'key': api_key,
                'part': 'snippet',
                #----↓フィルタ（いずれか1つ）↓-------
                #'allThreadsRelatedToChannelId':channelId,
                'videoId': video_id,
                #----↑フィルタ（いずれか1つ）↑-------
                'maxResults': '100',
                'moderationStatus': 'published',
                'order': 'relevance',
                'pageToken': nextPageToken,
                'searchTerms': '',
                'textFormat': 'plainText',
            }
            #リクエストURL作成
            target_url = URL_HEAD + (parse.urlencode(param))

            #データ取得
            res = requests.get(target_url).json()

            #件数
            item_count += len(res['items'])

            #print(target_url)
            print(str(item_count)+"件")

            #コメント情報を変数に格納
            for item in res['items']:
                items_output.append(
                    # [str(item['snippet']['topLevelComment']['snippet']['videoId'])]+
                    [str(item['snippet']['topLevelComment']['snippet']['textDisplay'].replace('\n', ''))] +
                    [str(item['snippet']['topLevelComment']['snippet']['textOriginal'])] +
                    [str(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])] +
                    # [str(item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])]+
                    # [str(item['snippet']['topLevelComment']['snippet']['authorChannelUrl'])]+
                    # [str(item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])]+
                    # [str(item['snippet']['topLevelComment']['snippet']['canRate'])]+
                    # [str(item['snippet']['topLevelComment']['snippet']['viewerRating'])]+
                    [str(item['snippet']['topLevelComment']['snippet']['likeCount'])] +
                    [str(item['snippet']['topLevelComment']['snippet']['publishedAt'])] +
                    [str(item['snippet']['topLevelComment']
                            ['snippet']['updatedAt'])]
                )

            #nextPageTokenがなくなったら処理ストップ
            if 'nextPageToken' in res:
                nextPageToken = res['nextPageToken']
            else:
                break

    #CSVで出力
    f = open(comment_list_dir + video_id + '-comments-list.csv', 'w', newline='', encoding='UTF-8')
    writer = csv.writer(f)
    writer.writerows(items_output)
    f.close()


def main(comment_list_dir, exe_num, api_key, video_id=None, video_json=None):
    os.makedirs(comment_list_dir, exist_ok=True)

    # ビデオIDを指定した場合
    if video_id != None:
        get_comment(video_id, exe_num, api_key)
    
    # jsonファイルを指定した場合
    elif video_json!=None:
        # jsonファイルを読み込んで、ビデオIDを抽出する
        with open(video_json) as f:
            jsn = json.load(f)
        
        video_ids = []
        [ video_ids.append(jsn['items'][i]['id']) for i in range(len(jsn['items'])) ]

        # チャンネルIDに対応する動画ごとにコメントをCSVファイルに保存する
        for video_id in video_ids:    
            get_comment(video_id, exe_num, api_key)

if __name__ == '__main__':
    comment_list_dir = sys.argv[1]
    exe_num = sys.argv[2]
    api_key = sys.argv[3]
    video_id = sys.argv[4]
    video_json = sys.argv[5]


    main(comment_list_dir, exe_num, api_key, video_id, video_json)
