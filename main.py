import base64
import io
import pandas as pd
from openai import OpenAI
from PIL import Image, ImageEnhance # 記得引入 ImageEnhance


# 1. 將伺服器網址指向你本機的 Ollama (預設通訊埠是 11434)
# api_key 在本機不需要真的金鑰，但套件規定一定要填寫一個字串，所以隨便寫即可
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', 
)





def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')




# 改良版：增加對比度與銳利度
def resize_and_encode_image(image_path, max_size=900): # 稍微調大一點點尺寸
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        
        # 1. 增強對比度 (讓字更黑、紙更白)
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(2.0)
        
        # 2. 增強銳利度 (讓邊緣更清晰)
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(2.0)

        img.thumbnail((max_size, max_size))
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')


def main():
    image_path = "sample.jpg" # 你的照片檔名
    
    print("正在將圖片編碼...")
    try:
        base64_image = resize_and_encode_image(image_path)
    except FileNotFoundError:
        print(f"找不到圖片檔案：{image_path}")
        return

    print("正在呼叫本機 Ollama (qwen2-vl) 進行表格辨識，請稍候...")
    print("（提示：本機辨識速度取決於你的電腦顯示卡與 CPU 效能）")

    # 2. 呼叫本機模型
    # 2. 呼叫本機模型
    response = client.chat.completions.create(
        model="qwen3-vl", # 確保你的模型名稱是正確的
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": """請分析這張圖片的內容，並將其轉換為 CSV 格式。這可能是一份表格或清單。

請嚴格遵循以下步驟執行：
步驟 1：觀察資料。判斷這份資料應該有哪些欄位（例如：如果是記帳可能是「日期,金額,備註」；如果是名片可能是「姓名,電話」），並將你決定的欄位名稱作為 CSV 的第一行。
步驟 2：逐行讀取。將圖片中的資料，依照你剛剛定義的欄位順序填入。
步驟 3：處理例外。如果有無法歸類的獨立文字或數字，請放在你定義的最後一個欄位（例如備註欄）。

【嚴格輸出格式】：
- 請只輸出純 CSV 內容。
- 絕對不要寫出「步驟 1...」等思考過程，也不要加上 ```csv 標籤。
- 直接以欄位名稱作為輸出的第一行。"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        extra_body={"options": {"num_ctx": 8192}}
    )

    csv_data = response.choices[0].message.content.strip()

    # 清理多餘標籤
    if csv_data.startswith("```"):
        csv_data = "\n".join(csv_data.split("\n")[1:-1])

    print("\n--- 本機 AI 辨識出的 CSV 資料 ---")
    print(csv_data)

    # 3. 轉存成 Excel
    try:
        df = pd.read_csv(io.StringIO(csv_data))
        output_filename = "output_ollama.xlsx"
        df.to_excel(output_filename, index=False)
        print(f"\n✅ 成功！已在本地端完成轉檔並存為 {output_filename}")
    except Exception as e:
        print(f"\n❌ 轉換成 Excel 失敗：{e}")

if __name__ == "__main__":
    main()