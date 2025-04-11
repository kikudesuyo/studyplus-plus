### スタディプラスの CLI 実装

### 今後の実装内容

- CLI で勉強の投稿をする
  必要な情報
  - AccessToken

基本的には認証さえうまく行けば、後は簡単。
教材も多分一覧からレスポンスで受け取っているはずなので、コピペするだけ。

### セットアップ方法

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
