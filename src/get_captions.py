'''
JSONファイルから字幕を取得する処理

'''
from youtube_transcript_api import YouTubeTranscriptApi
import csv
import json
import os
import sys

def main(caption_dir, video_json):
    out_dir = caption_dir + "/" + os.path.splitext(os.path.basename(video_json))[0]
    os.makedirs(out_dir, exist_ok=True)
    
    with open(video_json) as f:
        jsn = json.load(f)
    
    video_ids = []
    [ video_ids.append(jsn['items'][i]['id']) for i in range(len(jsn['items'])) ]

    for video_id in video_ids:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except:
            print(f"{video_id} doesn't have a transcript")
        
        caption = []
        for transcript in transcript_list:
            for tr in transcript.fetch():
                caption.append(tr)
        #CSVで出力
        f = open(out_dir + "/" +  video_id + '-captions-list.csv', 'w', newline='', encoding='UTF-8')
        writer = csv.DictWriter(f, fieldnames=['text', 'start', 'duration'])
        writer.writeheader()
        writer.writerows(caption)


if __name__ == '__main__':
    caption_dir = sys.argv[1]
    video_json = sys.argv[2]

    main(caption_dir, video_json)
