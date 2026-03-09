import streamlit as st
import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv

# 加載環境變數 (本地測試用)
load_dotenv()

# Supabase 設定
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# 初始化 Supabase 客戶端
@st.cache_resource
def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("請設定 SUPABASE_URL 和 SUPABASE_KEY 環境變數。")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# 設定頁面配置
st.set_page_config(page_title="即時監控系統", layout="wide")

st.title("🚀 即時監控儀表板 (Supabase + Streamlit)")

# --- 導覽列 ---
page = st.sidebar.radio("選擇功能頁面", ["用戶輸入區", "管理儀表板"])

if page == "用戶輸入區":
    # --- 側邊欄：用戶輸入區 ---
    st.sidebar.header("📥 數據輸入")
    with st.sidebar.form("input_form", clear_on_submit=True):
        sensor_value = st.number_input("輸入感測器數值", min_value=0, max_value=100, value=50)
        submitted = st.form_submit_button("發送數據")

        if submitted:
            try:
                data = {"value": sensor_value}
                response = supabase.table("sensor_data").insert(data).execute()
                st.sidebar.success(f"成功發送數值: {sensor_value}")
                st.rerun() # 立即刷新顯示新數據
            except Exception as e:
                st.sidebar.error(f"發送失敗: {e}")
    
    st.info("請在左側輸入數值並發送至資料庫。")

else:
    # --- 主畫面：管理儀表板 ---
    st.header("📊 管理儀表板 (即時監控)")

    # 建立預留容器以實現即時刷新
    placeholder = st.empty()

    def fetch_and_display():
        with placeholder.container():
            try:
                # 讀取最新的 10 筆資料，明確依照 created_at 降冪排序
                response = supabase.table("sensor_data").select("*").order("created_at", desc=True).limit(10).execute()
                df_data = response.data

                if df_data:
                    latest_value = df_data[0]["value"]
                    
                    # 警示內容判斷
                    if latest_value >= 55:
                        st.error(f"🚨 危險：數值過高！(目前數值：{latest_value})")
                    else:
                        st.success(f"✅ 系統正常：目前數值為 {latest_value}")

                    # 顯示數據表格
                    st.subheader("📋 最新 10 筆監測記錄 (由新到舊)")
                    
                    # 格式化表格顯示
                    display_data = []
                    for row in df_data:
                        display_data.append({
                            "ID": row["id"],
                            "時間": row["created_at"],
                            "感測數值": row["value"]
                        })
                    st.table(display_data)
                else:
                    st.warning("⚠️ 目前資料庫中尚無數據記錄。")

            except Exception as e:
                st.error(f"讀取數據失敗: {e}")

    # 執行首次顯示
    fetch_and_display()

    # 實作輕量級自動重整 (每 5 秒刷新一次)
    time.sleep(5)
    st.rerun()
