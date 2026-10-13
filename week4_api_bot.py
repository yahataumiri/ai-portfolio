from openai import OpenAI
import sys

# ========== 配置信息 ==========
ARK_API_KEY = "ark-3d32d546-13bc-4204-85c0-6af2e9180e17-ad097"
MODEL = "ep-20261013001457-xnqgl"
# ==============================

client = OpenAI(
    api_key=ARK_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def ask_llm(question):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user", "content": question}]
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python week4_api_bot.py \"你的问题\"")
    else:
        q = sys.argv[1]
        ans = ask_llm(q)
        print(ans)
        # 追加写入日志
        with open("chat_log.txt","a",encoding="utf-8") as f:
            f.write(f"问题：{q}\n回答：{ans}\n---------\n")