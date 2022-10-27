API_KEY = AIzaSyBrAzLo8_3WaQf7rYd_5KHJ6m6aY2TXExY
VIDEO_ID = zkoAgK7qN-M
VIDEO_JSON = ./Data/Video/Top_Video/youtubetop5.json


#########################################################################
#                             急上昇動画を取得                            #
#########################################################################
TOP_VIDEO_DIR = ./Data/Video/Top_Video
VIDEO_NUM = 100
TOP:
	python src/get_top_video.py ${TOP_VIDEO_DIR} ${VIDEO_NUM} ${API_KEY}


#########################################################################
#               キーワードを含むタイトルの動画を再生回数順で取得                #
#########################################################################
KEYWORD_VIDEO_DIR = ./Data/Video/Keyword_Video
KEYWORD = 大公開
KEY:
	python src/get_keyword_video.py ${TOP_VIDEO_DIR} ${KEYWORD} ${API_KEY}


#########################################################################
#                               コメント                                 #
#########################################################################
COMMENT_LIST_DIR = ./Data/Corpus/Comment_List
EXE_NUM = 100
# ビデオIDからコメント一覧を取得する処理
COMMENT_ID:
	python src/get_comment.py ${COMMENT_LIST_DIR} ${EXE_NUM} ${API_KEY} ${VIDEO_ID}

# 複数の動画データが保存されたJSONファイルからコメント一覧を取得する処理 
COMMENT_JSON:
	python src/get_comment.py ${COMMENT_LIST_DIR} ${EXE_NUM} ${API_KEY} ${VIDEO_JSON}


#########################################################################
#                              字幕                                     #
#########################################################################
CAPTION_DIR = ./Data/Corpus/Caption
# ビデオIDから字幕を取得する処理
CAPTION_ID:
	python src/get_caption.py ${CAPTION_DIR} ${VIDEO_ID}

# 複数の動画データが保存されたJSONファイルから字幕を取得する処理
CAPTION_JSON:
	python src/get_captions.py ${CAPTION_DIR} ${VIDEO_JSON}