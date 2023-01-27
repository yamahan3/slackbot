from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import openai
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

# APIキーを取得
openai.api_key = os.environ['OPENAI_TOKEN']

#モデルを指定
model_engine = "text-davinci-003"

# チャンネルでメンションされた時
@app.event("app_mention")
def mention_handler(body, say):
    # 入力された内容を取得
    prompt = body['event']['text']
    
    #推論結果を出力
    message = create_completion(prompt)
    say(message)


# ダイレクトメッセージが送られたとき
@app.event("message")
def mention_handler(body, say):
    # 入力された内容を取得
    prompt = body['event']['text']

    #推論結果を出力
    message = create_completion(prompt)
    say(message)

#推論を実行
def create_completion(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    #推論結果を出力
    message = completions.choices[0].text

    return message

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
