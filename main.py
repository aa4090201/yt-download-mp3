import requests
from bs4 import BeautifulSoup
import re
   
import yt_dlp 
#pip install yt_dlp
# ffmpeg
# https://www.ffmpeg.org/download.html

# 需要import requests, BeautifulSoup, re, os, csv
from find_artist_all_songs import find_artist_all_songs
from find_first_year_song import find_first_year_song
from find_hit_song import find_hit_song
from kworb_to_youtube import kworb_to_youtube
from download_yt import download_mp3
from save_to_csv import save_to_csv

# 給定歌手的kworb的網址 https://kworb.net/youtube/artist/歌手頻道名.html
url = "https://kworb.net/youtube/artist/badbunny.html"
# 找出該歌手的所有歌曲數據 回傳包含連結 歌曲名稱 總觀看數 昨日觀看數 發布時間(年/月) 
# video_data = {
#                     'link': absolute_link,
#                     'video_name': video_name,
#                     'total_views': total_views,
#                     'yesterday_views': yesterday_views,
#                     'release_date': release_date
#                 }
# 回傳的是List of dictionary
videos_data = find_artist_all_songs(url)

# 回傳一個從發布時間最小到12個月後的的歌曲的List
first_year = find_first_year_song(videos_data)

# 從list找出成名曲 (目前是第一年中現在總觀看最高的歌曲)
hit_song = find_hit_song(first_year) 


# 給kowrb有嵌入式yt影片歌曲的網址 https://kworb.net/youtube/video/影片id.html
# 回傳頻道id及影片id
channel_name, video_id = kworb_to_youtube(hit_song[0]['link'])

# 將頻道id加進youtube網址
video_url = f'https://www.youtube.com/watch?v={video_id}'

# 從youtube網址 用yt-dl下載youtube影片並且使用ffmpeg轉成mp3格式放進./music資料夾 
# 回傳檔案名稱及音樂檔案位置
file_name,file_path = download_mp3(video_url)

# 給定檔案路徑 檔案名稱 影片id 頻道名稱(不含@)將上述轉成csv檔案
save_to_csv(file_path, file_name, video_id, channel_name)
