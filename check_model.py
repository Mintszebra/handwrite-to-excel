from google import genai


API_KEY = "YOUR_API_KEY"

client = genai.Client(api_key=API_KEY)

print("正在查詢可用的模型清單...\n")
for model in client.models.list():
    #只列出支援文字與圖片生成的模型
    if "generateContent" in model.supported_actions:
        print(f"可用模型名稱: {model.name}")