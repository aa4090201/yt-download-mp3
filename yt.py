import requests
from bs4 import BeautifulSoup
import re
import json     
import yt_dlp #要裝yt_dlp 跟 ffmpeg
import os
import csv


import requests
from bs4 import BeautifulSoup
from datetime import datetime


url = "https://kworb.net/youtube/artist/badbunny.html"
def find_artist_all_songs(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 發送 HTTP 請求到目標網頁
    response = requests.get(url, headers=headers)
    
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    rows = soup.find_all('tr')
    
    # 初始化列表來存儲數據
    videos_data = []
    
    # 遍歷每個 <tr>，提取數據
    for tr in rows:
        # 提取第一個 <td> 裡的超鏈接和影片名稱
        td1 = tr.find('td', class_='text')
        if td1:
            link_tag = td1.find('a')
            if link_tag:
                relative_link = link_tag['href']  # 網頁連結（相對路徑）
                video_name = link_tag.text.strip()  # 影片名稱
    
                # 將相對鏈接轉換為絕對鏈接
                absolute_link = url.split('artist')[0] + relative_link.replace('../', '')  # 拼接完整網址
    
                # 提取第二個 <td> 的總觀看次數
                total_views = tr.find_all('td')[1].text.strip()
    
                # 提取第三個 <td> 的昨日觀看次數
                yesterday_views = tr.find_all('td')[2].text.strip()
    
                # 提取第四個 <td> 的發布時間
                release_date = tr.find_all('td')[3].text.strip()
    
                # 儲存為字典
                video_data = {
                    'link': absolute_link,
                    'video_name': video_name,
                    'total_views': total_views,
                    'yesterday_views': yesterday_views,
                    'release_date': release_date
                }
    
                # 將字典加入列表
                videos_data.append(video_data)
    return videos_data
# 顯示結果


def find_first_year_song(videos_data):
    for video in videos_data:
        video['release_date'] = datetime.strptime(video['release_date'], '%Y/%m')
    min_date = min(video['release_date'] for video in videos_data)

    # 計算範圍的結束日期（最小日期 + 1年）
    end_date = min_date.replace(year=min_date.year + 1)
    
    # 篩選出符合範圍的資料
    filtered_videos = [video for video in videos_data if min_date <= video['release_date'] <= end_date]
    
    # 顯示篩選後的結果

    return filtered_videos

def find_hit_song(videos_data): 
    # 轉換 total_views 字串為整數並找出最大值
    for video in videos_data:
        # 清除數字中的逗號，並轉換為整數
        video['total_views'] = int(video['total_views'].replace(',', ''))
    
    # 找出最大觀看次數的影片
    max_views = max(video['total_views'] for video in videos_data)
    
    # 篩選出擁有最大觀看次數的影片
    hit_song = [video for video in videos_data if video['total_views'] == max_views]
    
    # 返回這些影片
    return hit_song




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



videos_data = find_artist_all_songs(url)
# for video in videos_data:
#     print(video['link'])
first_year = find_first_year_song(videos_data)
hit_song = find_hit_song(first_year) 


# 你的 kworb 網址
kworb_url = 'https://kworb.net/youtube/video/0VR3dfZf9Yg.html'
channel_name, video_id = kworb_to_youtube(hit_song[0]['link'])
video_url = f'https://www.youtube.com/watch?v={video_id}'
file_name,file_path = download_mp3(video_url)
save_to_csv(file_name, video_id, channel_name, file_path)
