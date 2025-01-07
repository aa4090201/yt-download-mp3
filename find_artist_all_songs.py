import requests
from bs4 import BeautifulSoup

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