import requests
from bs4 import BeautifulSoup
import re
import json     
import yt_dlp #要裝yt_dlp 跟 ffmpeg
import os
import csv

def kworb_to_youtube(kworb_url):

    # 使用正則表達式提取 video_id
    match = re.search(r'https://kworb\.net/youtube/video/([a-zA-Z0-9_-]+)\.html', kworb_url)

    if match:
        # 提取 video_id
        video_id = match.group(1)
        
        # 構造新的 embed 網址
        embed_url = f'https://www.youtube.com/embed/{video_id}?rel=0'
        
        print(f'嵌入影片網址: {embed_url}')
    else:
        print('無法從提供的網址中提取 video_id')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # 發送 HTTP 請求到目標網頁
    response = requests.get(embed_url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    # 找到所有的 <script> 標籤
    scripts = soup.find_all('script')

    # 遍歷 <script> 標籤並查找包含 'ytcfg.set' 的腳本
    for script in scripts:
        # 檢查 script.string 是否為 None
        if script.string and 'ytcfg.set' in script.string:
            # 使用正則表達式提取 JSON 字符串
            match = re.search(r'ytcfg\.set\(({.*?})\);', script.string)
            if match:
                json_data = match.group(1)
                data = json.loads(json_data)

                # 假設 data 中包含影片網址，提取並打印
                # 具體結構根據實際情況而定
                video_id = data.get('VIDEO_ID')
                if video_id:
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    print(f'影片網址: {video_url}')




    response = requests.get(video_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    scripts = soup.find_all('script')

    # 遍歷 <script> 標籤並查找包含 'ytInitialPlayerResponse' 的腳本
    for script in scripts:
        if script.string and 'ytInitialPlayerResponse' in script.string:
            # 使用正則表達式提取 JSON 字符串
            match = re.search(r'ytInitialPlayerResponse\s*=\s*(\{.*?\});', script.string)
            if match:
                json_data = match.group(1)
                data = json.loads(json_data)
                
                # 打印 JSON 資料
                # print(json.dumps(data, indent=4))
                
                # 提取 ownerProfileUrl
                owner_profile_url = data.get('microformat', {}).get('playerMicroformatRenderer', {}).get('ownerProfileUrl', '')
                
                if owner_profile_url:
                    # 提取 '@' 後的頻道名稱
                    channel_name = owner_profile_url.split('@')[-1]
                    print(f'頻道名稱: {channel_name}')
                else:
                    print('未找到頻道名稱')



    return channel_name, video_id



def download_mp3(url):
    if not os.path.exists('music'):
        os.makedirs('music')
    
    # 設定下載的檔案路徑
    output_path = 'music/%(title)s.%(ext)s'

    ydl_opts = {
        'format': 'bestaudio/best',  # 下載最佳音質
        'outtmpl': output_path,  # 設定下載的檔案名稱
        'embed-thumbnail': True,  # 嵌入縮圖
        'add-metadata': True,  # 添加影片元資料
        'extract-audio': True,  # 只提取音訊
        'audio-format': 'mp3',  # 強制轉換為 MP3 格式
        'audio-quality': '320K',  # 設定音質為 320kbps
        'postprocessors': [{  # 轉換音訊為 MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    # 下載並取得檔案名稱
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 執行下載並提取資訊
        info_dict = ydl.extract_info(url, download=True)
        # 取得標題與檔案副檔名
        title = info_dict.get('title', None)
        file_ext = 'mp3'  # 強制設定副檔名為 mp3

    # 生成實際檔案名稱
    downloaded_file_name = f"{title}.{file_ext}"

    # 返回檔案名稱及路徑
    file_location = os.path.abspath(os.path.join('music', downloaded_file_name))
    print(f"檔案已下載並儲存在: {file_location}")
    
    return downloaded_file_name, file_location



def save_to_csv(file_path, file_name, video_id, channel_name, filename="output.csv"):
    # 開啟 CSV 檔案進行寫入，若檔案不存在則會創建
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 如果檔案是空的，可以寫入標題
        if file.tell() == 0:
            writer.writerow(['File Path', 'File Name', 'Video ID', 'Channel Name'])
        
        # 寫入一行資料
        writer.writerow([file_path, file_name, video_id, channel_name])
    print("資料已成功保存到 output.csv")


# 你的 kworb 網址
kworb_url = ''
channel_name, video_id = kworb_to_youtube(kworb_url)
video_url = f'https://www.youtube.com/watch?v={video_id}'
file_name,file_path = download_mp3(video_url)
save_to_csv(file_name, video_id, channel_name, file_path)
