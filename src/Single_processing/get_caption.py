'''
ビデオIDから字幕を取得する処理

'''
from youtube_transcript_api import YouTubeTranscriptApi
import csv
import json
import os
import sys

def main(caption_dir, video_id):
    out_dir = caption_dir + "/each"
    os.makedirs(out_dir, exist_ok=True)
    
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except:
        print(f"{video_id} doesn't have a transcript")

    caption = []
    for transcript in transcript_list:
        for tr in transcript.fetch():
            caption.append(tr)
    #CSVで出力
    f = open(out_dir + "/" + video_id + '-captions-list.csv', 'w', newline='', encoding='UTF-8')
    writer = csv.DictWriter(f, fieldnames=['text', 'start', 'duration'])
    writer.writeheader()
    writer.writerows(caption)


if __name__ == '__main__':
    caption_dir = sys.argv[1]
    video_id = sys.argv[2]

    main(caption_dir, video_id)
