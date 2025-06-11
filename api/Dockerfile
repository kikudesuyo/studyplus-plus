FROM python:3.12-slim
WORKDIR /app

# Litestream CLI のバージョンを指定

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ ./


# Litestream CLI をインストール
ENV LITESTREAM_VERSION=v0.3.13
ADD https://github.com/benbjohnson/litestream/releases/download/$LITESTREAM_VERSION/litestream-$LITESTREAM_VERSION-linux-amd64.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

# litestream の設定ファイルと実行スクリプト (後述) をコピー
COPY api/litestream.yml /etc/litestream.yml
COPY api/run.sh /app/run.sh

RUN chmod +x /app/run.sh

EXPOSE 8080
# 起動スクリプトを実行する
CMD ["/app/run.sh"]