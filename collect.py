import os
import datetime
import requests
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
date_jp = today.strftime("%Y年%m月%d日")

# NewsAPI or web search via OpenAI web search capability
def fetch_news():
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたはAI・テクノロジーニュースのキュレーターです。"
                    "本日の最新AIニュースを調査し、日本語で詳しくまとめてください。"
                    "各ニュースには概要と関連URLを含めてください。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"本日 {date_jp} のAI関連ニュースを以下の形式でMarkdownにまとめてください。\n\n"
                    "# AI ニュース {date_jp}\n\n"
                    "## [ニュースタイトル]\n"
                    "概要説明\n\n"
                    "**出典**: URL\n\n"
                    "---\n\n"
                    "カバーすべきトピック:\n"
                    "- 新しいAIモデル・サービスのリリース\n"
                    "- 主要AI企業（OpenAI, Google, Anthropic, Meta, Microsoft等）の動向\n"
                    "- AI研究・論文の注目発表\n"
                    "- AI規制・政策の動向\n"
                    "- 日本国内のAI関連ニュース\n"
                    "10件以上のニュースを含めてください。"
                )
            }
        ],
        max_tokens=4000,
    )
    return response.choices[0].message.content

content = fetch_news()

# ヘッダーとフッターを整形
output = f"# AI ニュース {date_jp}\n\n"
output += content.strip()
output += f"\n\n---\n*自動生成: {date_str}*\n"

filename = f"{date_str}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Saved: {filename}")
