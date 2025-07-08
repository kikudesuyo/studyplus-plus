## 使用技術:

![My Skills](https://skillicons.dev/icons?i=sqlite)

## DB 接続の取り扱い:

- `api/repository/init_db.py`で DB 接続を管理
- リポジトリ層の関数には SQLite の接続オブジェクト(`db`)を引数として注入
- リポジトリ層では db のクローズ(`db.close()`)は行わず、サービス層で実装

## 注意点

- サービス層で DB の開閉を行うため、リポジトリ層で `db.close()` を呼ぶとエラーが発生する
- トランザクション（`commit` や `rollback`）の管理もサービス層の責任範囲であるため、リポジトリ層では行わない
