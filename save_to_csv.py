import csv

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
