<img src="https://github.com/user-attachments/assets/10cddd4f-447a-44b0-abf9-c3a41bdeee82" alt="My Skills" width="60" />

### スタディプラスの 拡張

### 今後の実装内容

- CLI で勉強の投稿をする
  必要な情報
  - AccessToken

### セットアップ方法

#### 仮想環境セットアップ

```bash
cd studyplus-plus/
#仮想環境作成
python -m venv .venv

#仮想環境有効化
source .venv/bin/activate

#ライブラリのインストール
pip install -r requirements.txt
#(任意)環境変数の登録(main.py以外でもファイル実行を可能にさせる)
.venv/bin/activateにて`YOUR_PATH`を指定して下記を記述してください
#環境変数を追加
export PYTHONPATH="YOUR_PATH/studyplus-plus/api:$PYTHONPATH"
```

#### .env ファイル作成

```
cp -p .env.example .env
```

#### .env ファイルの編集

- `CONSUMER_KEY`,`CONSUMER_SECRET` は直接渡すので連絡してください。

- `STUDYPLUS_EMAIL`,`STUDYPLUS_PASSWORD`は **Studyplus** に登録している情報を入力してください。

- `GEMINI_API_KEY` は 登録した **Gemini** の API キーを入力してください。

```env
#### 注意

`CONSUMER_KEY`,`CONSUMER_SECRET`ユーザーに関わらず一意なことは確認済み。
定期的に更新されるのかを今後確認する必要があります。

### 使用技術

![My Skills](https://skillicons.dev/icons?i=python)
```
