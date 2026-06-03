import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime

def deep_scrape_steamcharts_fixed(limit_games=25):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    # Mức 1: Lấy danh sách game từ trang chủ
    top_url = "https://steamcharts.com/top/p.1"
    print("Mức 1: Đang quét danh sách game hàng đầu trên Steamcharts...")
    
    try:
        response = requests.get(top_url, headers=headers)
        if response.status_code != 200:
            print("Không thể truy cập trang chủ Steamcharts. Vui lòng kiểm tra lại mạng.")
            return None, None
        
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="common-table")
        if not table:
            print("Không tìm thấy bảng danh sách tổng hợp.")
            return None, None
            
        rows = table.find_all("tr")[1:]
        
        game_urls = []
        for row in rows[:limit_games]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                link_tag = cols[1].find("a")
                if link_tag:
                    game_urls.append({
                        "Game_Name": link_tag.text.strip(),
                        "Detail_URL": "https://steamcharts.com" + link_tag["href"]
                    })
    except Exception as e:
        print(f"Lỗi khi lấy danh sách tổng hợp: {e}")
        return None, None

    player_count_trend_list = []
    game_details_dim_list = []
    
    print(f"\nMức 2: Tiến hành vào chi tiết từng game để lấy dữ liệu chuỗi thời gian (Mục tiêu: {len(game_urls)} game)...")
    
    for idx, game in enumerate(game_urls, 1):
        print(f"[{idx}/{len(game_urls)}] Đang cào lịch sử của: {game['Game_Name']}...")
        
        try:
            res = requests.get(game["Detail_URL"], headers=headers)
            if res.status_code != 200:
                print(f"-> Bỏ qua game {game['Game_Name']} do lỗi kết nối (HTTP {res.status_code})")
                continue
                
            detail_soup = BeautifulSoup(res.text, "html.parser")
            
            # --- TÌM BẢNG LỊCH SỬ (Cập nhật cơ chế tìm kiếm linh hoạt) ---
            # Thử tìm bảng bằng class phổ biến hoặc tìm tất cả các bảng trên trang
            chart_table = detail_soup.find("table", class_="common-table") or detail_soup.find("table")
            
            if chart_table:
                chart_rows = chart_table.find_all("tr")[1:]  # Bỏ hàng tiêu đề (Tháng, Số người chơi,...)
                
                rows_extracted = 0
                for c_row in chart_rows:
                    c_cols = c_row.find_all("td")
                    if len(c_cols) >= 5:
                        month_year = c_cols[0].text.strip()
                        avg_players = c_cols[1].text.strip().replace(",", "")
                        gain_loss_raw = c_cols[2].text.strip().replace("%", "").replace("+", "")
                        peak_players = c_cols[4].text.strip().replace(",", "")
                        
                        # Chuyển đổi kiểu dữ liệu an toàn
                        try:
                            avg_players_num = float(avg_players) if avg_players != "-" else 0.0
                            peak_players_num = int(peak_players) if peak_players != "-" else 0
                            gain_loss_num = float(gain_loss_raw) / 100.0 if (gain_loss_raw != "-" and gain_loss_raw != "") else 0.0
                        except ValueError:
                            continue
                            
                        player_count_trend_list.append({
                            "Game_Name": game["Game_Name"],
                            "Month_Year": month_year,
                            "Avg_Players": avg_players_num,
                            "Gain_Loss_Percent": gain_loss_num,
                            "Peak_Players": peak_players_num
                        })
                        rows_extracted += 1
                
                # Nếu lấy thành công lịch sử của game này, thì mới thêm vào bảng Dimension (Game_Details_Dim)
                if rows_extracted > 0:
                    app_id = game["Detail_URL"].split("/")[-1]
                    game_details_dim_list.append({
                        "Game_Name": game["Game_Name"],
                        "Steam_App_ID": app_id,
                        "Genre": "PC Game",
                        "Developer": "Steam Publisher",
                        "Release_Date": "N/A",
                        "Current_Price": "Check Store"
                    })
            
            # Nghỉ ngắn 1 giây để bảo vệ tiến trình cào không bị tường lửa chú ý
            time.sleep(1)
            
        except Exception as e:
            print(f"Lỗi phát sinh khi xử lý chi tiết game {game['Game_Name']}: {e}")
            continue

    df_trend = pd.DataFrame(player_count_trend_list)
    df_dim = pd.DataFrame(game_details_dim_list)
    
    return df_trend, df_dim

if __name__ == "__main__":
    # Để kiểm tra nhanh, tôi đặt giới hạn cào thử 15 game hàng đầu (bạn có thể tăng lên tùy ý)
    df_trend, df_dim = deep_scrape_steamcharts_fixed(limit_games=15)
    
    if (df_trend is not None) and (not df_trend.empty):
        # Tự động định vị thư mục Desktop bao gồm cả OneDrive
        home_dir = os.path.expanduser("~")
        possible_desktop_paths = [
            os.path.join(home_dir, "OneDrive", "Máy tính"),
            os.path.join(home_dir, "OneDrive", "Desktop"),
            os.path.join(home_dir, "Desktop")
        ]
        desktop_path = next((path for path in possible_desktop_paths if os.path.exists(path)), os.path.dirname(os.path.abspath(__file__)))
        
        trend_file_path = os.path.join(desktop_path, "Player_Count_Trend.csv")
        dim_file_path = os.path.join(desktop_path, "Game_Details_Dim.csv")
        
        # Xuất dữ liệu
        df_trend.to_csv(trend_file_path, index=False, encoding="utf-8-sig")
        df_dim.to_csv(dim_file_path, index=False, encoding="utf-8-sig")
        
        print("\n--- THÀNH CÔNG ---")
        print(f"1. Đã tạo bảng Fact tại: {trend_file_path} (Tổng cộng {len(df_trend)} dòng lịch sử theo tháng)")
        print(f"2. Đã tạo bảng Dim tại: {dim_file_path} (Tổng cộng {len(df_dim)} bản ghi thông tin game)")
    else:
        print("\n--- THẤT BẠI ---")
        print("Vẫn chưa thể trích xuất được dữ liệu. Hãy kiểm tra xem màn hình Terminal có báo lỗi kết nối cụ thể nào không.")