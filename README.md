<img src="" alt="My Skills" width="100" />

### スタディプラスの CLI 実装

### 今後の実装内容

- CLI で勉強の投稿をする
  必要な情報
  - AccessToken

### セットアップ方法

#### 仮想環境セットアップ

```bash
cd studyplus-cli/
#仮想環境作成
python -m venv .venv
#仮想環境有効化
source .venv/bin/activate
#ライブラリのインストール
pip install -r requirements.txt
#(任意)環境変数の登録(main.py以外でもファイル実行を可能にさせる)
.venv/bin/activateにて`YOUR_PATH`を指定して下記を記述してください
#環境変数を追加
export PYTHONPATH="YOUR_PATH/studyplus-cli/src:$PYTHONPATH"
```

#### .env ファイル作成

```
cp -p .env.example .env
```

#### .env ファイルの編集

- `CONSUMER_KEY`,`CONSUMER_SECRET` は直接渡すので連絡してください。
- `STUDYPLUS_EMAIL`,`STUDYPLUS_PASSWORD`は **Studyplus** に登録している情報を入力してください。

#### 注意

`CONSUMER_KEY`,`CONSUMER_SECRET`ユーザーに関わらず一意なことは確認済み。
定期的に更新されるのかを今後確認する必要があります。

### 使用技術

[![My Skills](https://skillicons.dev/icons?i=python)]
