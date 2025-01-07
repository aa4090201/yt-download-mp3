from datetime import datetime

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