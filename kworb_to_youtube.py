import requests
from bs4 import BeautifulSoup
import re
import json  

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
    # print(soup)
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
                    embed_url = f'https://kworb.net/youtube/video/{video_id}.html'
                    response = requests.get(embed_url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    artistsong_name = soup.find('span', style='display: inline-block; vertical-align: middle; max-width: 450px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;')
    
                    if artistsong_name:
                        name = "未找到頻道名稱，影片名稱："+artistsong_name.get_text()
                        return name, video_id

                    else:
                        print("未找到目標標籤")
                        return '未找到頻道名稱', video_id




    return channel_name, video_id

print(kworb_to_youtube("https://kworb.net/youtube/video/bM7SZ5SBzyY.html"))


