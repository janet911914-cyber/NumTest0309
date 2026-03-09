-- Supabase 建立資料表 SQL 指令
-- 請在 Supabase 控制台的 SQL Editor 中執行以下代碼

-- 建立 sensor_data 資料表
CREATE TABLE IF NOT EXISTS sensor_data (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  value INT NOT NULL
);

-- (選填) 啟用即時監控 (Realtime)
-- 雖然 Streamlit 程式碼是透過輪詢讀取，但啟用此功能可方便未來擴充
-- ALTER PUBLICATION supabase_realtime ADD TABLE sensor_data;

-- 插入一筆測試數據
INSERT INTO sensor_data (value) VALUES (50);

-- 確認資料表內容
SELECT * FROM sensor_data;
