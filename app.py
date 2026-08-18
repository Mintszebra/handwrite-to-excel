import streamlit as st
import pandas as pd
import io
from PIL import Image
from google import genai

# 設定網頁標題與排版 (這會讓手機版看起來更像 App)
st.set_page_config(page_title="手寫記帳轉 Excel ", page_icon="📝", layout="centered")

# --- 網頁側邊欄 (設定區) ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("請輸入 Google Gemini API Key", type="password", help="免費取得：https://aistudio.google.com/")
    st.markdown("---")
    st.markdown("### 💡 關於此專案")
    st.markdown("透過 Gemini 3.5 Flash 視覺大模型，自動將手寫記帳單轉換為結構化的 Excel 報表。")

# --- 網頁主畫面 ---
st.title("手寫記帳 ➔ Excel 轉換器")
st.write("請上傳您的手寫記帳單照片，AI 將自動辨識並轉成 Excel 供您下載。")

# 建立檔案上傳區塊 (支援手機直接開啟相機)
uploaded_file = st.file_uploader("點擊上傳或拖曳圖片至此", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 顯示使用者上傳的圖片
    image = Image.open(uploaded_file)
    st.image(image, caption="已上傳的圖片", use_container_width=True)

    # 建立一個轉換按鈕
    if st.button("開始轉換為 Excel", type="primary"):
        
        if not api_key:
            st.error("請先在左側欄輸入您的 Gemini API Key！")
        else:
            with st.spinner("AI 正在努力辨識圖片中，請稍候..."):
                try:
                    # 1. 初始化 AI 客戶端
                    client = genai.Client(api_key=api_key)
                    
                    # 2. 設定 AI 提示詞 (使用我們之前討論出的泛化步驟版)
                    prompt = """
                    請分析這張圖片的內容，並將其轉換為 CSV 格式。
                    請嚴格遵循以下步驟執行：
                    步驟 1：判斷這份資料應該有哪些欄位（例如：日期,金額,備註），並將其作為 CSV 第一行。
                    步驟 2：逐行讀取。將圖片中的資料，依照欄位順序填入。遇到獨立的文字請放入備註。
                    
                    【嚴格輸出格式】：
                    - 請只輸出純 CSV 內容。
                    - 絕對不要寫出思考過程，也不要加上 ```csv 標籤。
                    """
                    
                    # 3. 呼叫 Gemini API
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[image, prompt]
                    )
                    
                    # 4. 清理並轉換資料
                    csv_data = response.text.strip()
                    if csv_data.startswith("```"):
                        csv_data = "\n".join(csv_data.split("\n")[1:-1])
                        
                    # 將 CSV 文字轉為 Pandas DataFrame
                    df = pd.read_csv(io.StringIO(csv_data))
                    
                    # 顯示辨識結果
                    st.success("✅ 轉換成功！預覽資料如下：")
                    st.dataframe(df, use_container_width=True)
                    
                    # 5. 製作 Excel 下載按鈕
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="下載 Excel 檔案",
                        data=excel_data,
                        file_name="手寫記帳轉換結果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"❌ 發生錯誤，請確認圖片是否清晰或 API Key 是否正確。詳細錯誤：{e}")