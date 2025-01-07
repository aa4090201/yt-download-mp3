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
