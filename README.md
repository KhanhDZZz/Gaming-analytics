# Gaming-analytics
Phân tích dữ liệu steam games thu thập tại trang web https://steamcharts.com
# Gaming Analytics - SQL Server & Power BI

## Mô tả
Dự án phân tích xu hướng người chơi các trò chơi từ năm 2012-2026 sử dụng SQL Server và Power BI.

## Cấu trúc dữ liệu
- **Player_Count_Trend**: Lịch sử lượng người chơi trung bình, peak, và thay đổi
- **Game_Details_Dim**: Thông tin chi tiết về từng trò chơi

## Cài đặt nhanh

```

Yêu cầu hệ thống
- SQL Server 2019 hoặc cao hơn
- Power BI Desktop (miễn phí từ Microsoft)
- Git

Insights chính
- Counter-Strike 2 và Dota 2 là hai game hàng đầu
- PUBG đạt peak cao nhất nhưng đang giảm trend
- Bongo Cat đang có momentum tích cực gần đây
- Có rõ ràng mẫu mùa vụ cho từng game

Cấu trúc Dashboard
- Overview: KPI chính (Avg Players, Peak, Games Up/Down)
- Trend Analysis: Line chart xu hướng qua thời gian
- Game Comparison: So sánh hiệu suất các game
- Detail Table: Dữ liệu chi tiết theo tháng
