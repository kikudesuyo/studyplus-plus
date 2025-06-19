#!/bin/sh
set -e

# もしローカルに古いデータベースファイルが存在していたら削除する
rm -f /app/studyplus-plus.db

# Google Cloud Storage からデータベースファイルを復元する
# 引数には復元先のローカルのデータベースファイルのパスを指定する (今回は `/app/studyplus-plus.db` としている)
# `-if-replica-exists` フラグを指定すると、レプリカが存在する場合にのみ復元を行う
# これを指定しないと、まだレプリカが存在しない場合 ( = 初回起動時 ) にエラーが発生する
# `-config` フラグに設定ファイルのパスを指定する
litestream restore -if-replica-exists -config /etc/litestream.yml /app/studyplus-plus.db

# Google Cloud Storage にデータベースファイルをレプリケートしてアプリケーションを起動する
# `-exec` フラグにアプリケーションの起動コマンドを指定する (今回はアプリケーションのバイナリのパスを指定している)
# `-config` フラグに設定ファイルのパスを指定する
litestream replicate -exec "uvicorn api.main:app --host 0.0.0.0 --port 8080" -config /etc/litestream.yml