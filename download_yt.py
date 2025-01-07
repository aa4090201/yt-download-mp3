import os
import yt_dlp 

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
