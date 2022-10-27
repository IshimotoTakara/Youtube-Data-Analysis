'''
${video_ids}内のそれぞれのビデオIDに対応する動画のコメントをCSVファイルに保存する。

'''
import requests
import urllib.parse as parse
import csv
import json
import os
import sys


def main(comment_list_dir, exe_num, api_key, video_json):
    out_dir = comment_list_dir + "/" + \
        os.path.splitext(os.path.basename(video_json))[0]
    os.makedirs(out_dir, exist_ok=True)

    # jsonファイルを読み込んで、ビデオIDを抽出する
    with open(video_json) as f:
        jsn = json.load(f)
    
    video_ids = []
    [ video_ids.append(jsn['items'][i]['id']) for i in range(len(jsn['items'])) ]

    # チャンネルIDに対応する動画ごとにコメントをCSVファイルに保存する
    for video_id in video_ids:    
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
        f = open(out_dir + "/" + video_id + '-comments-list.csv',
                'w', newline='', encoding='UTF-8')
        writer = csv.writer(f)
        writer.writerows(items_output)
        f.close()

if __name__ == '__main__':
    comment_list_dir = sys.argv[1]
    exe_num = int(sys.argv[2])
    api_key = sys.argv[3]
    video_json = sys.argv[4]


    main(comment_list_dir, exe_num, api_key, video_json)
