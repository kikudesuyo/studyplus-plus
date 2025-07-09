# 変数定義
GCP_PROJECT_ID = studyplus-plus
GCP_REGION = asia-northeast1
REPO_NAME = studyplus-plus

STUDYPLUS_ENV_FILE = studyplus-prod.yml

IMAGE_TAG = latest

# サービス定義
STUDYPLUS_SERVICE = studyplus-api
STUDYPLUS_IMAGE = $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(REPO_NAME)/$(STUDYPLUS_SERVICE):$(IMAGE_TAG)
STUDYPLUS_PLUS_SERVICE = studyplus-plus-db
STUDYPLUS_PLUS_DB_IMAGE = $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(REPO_NAME)/$(STUDYPLUS_PLUS_SERVICE):$(IMAGE_TAG)
# MCP_SERVICE = mcp-server
# MCP_IMAGE = $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(REPO_NAME)/$(MCP_SERVICE)


# GCP初期設定
.PHONY: setup-gcp

setup-gcp:
	gcloud artifacts repositories create $(REPO_NAME) \
		--repository-format=docker \
		--location=$(GCP_REGION) \
		--description="studyplus-plus application repository" \
		--project=$(GCP_PROJECT_ID) \
	gcloud auth configure-docker $(GCP_REGION)-docker.pkg.dev


# Studyplus-apiサーバー
.PHONY: push-studyplus deploy-studyplus

WEEKLY_BATTLE_JOB_ENDPOINT = "https://studyplus-api-445395497817.asia-northeast1.run.app/weekly-study-battle"
BOT_LIKE_JOB_ENDPOINT = "https://studyplus-api-445395497817.asia-northeast1.run.app/timeline/followees/records/like/bot"

DEV_DB_PATH = api/studyplus-plus.db

dev:
	DB_PATH=$(DEV_DB_PATH) uvicorn api.main:app --reload 


push-studyplus:
	docker build --platform linux/amd64 -f api/Dockerfile -t $(STUDYPLUS_IMAGE) .
	docker push $(STUDYPLUS_IMAGE)

deploy-studyplus:
	gcloud run deploy $(STUDYPLUS_SERVICE) \
		--image $(STUDYPLUS_IMAGE) \
		--region $(GCP_REGION) \
		--project $(GCP_PROJECT_ID) \
		--allow-unauthenticated \
		--env-vars-file=$(STUDYPLUS_ENV_FILE) \
		--max-instances=1 \
		--min-instances=0 \
		--memory=256Mi \
		--timeout=30s \

studyplus-all: push-studyplus deploy-studyplus


#毎週日曜日19:00(日本時間は月曜日の04:00)に勉強結果をStudyplusに投稿する
cron-weekly-study-battle:
	gcloud scheduler jobs create http register-weekly-battle-job \
		--location=$(GCP_REGION) \
		--description="1週間の勉強結果をStudyplusにPOSTする" \
		--schedule="0 19 * * 0" \  
		--uri ${WEEKLY_BATTLE_JOB_ENDPOINT} \
		--http-method=POST \
		--time-zone="UTC" \
		--project=$(GCP_PROJECT_ID) \

#miyavinがユーザーの学習記録にいいねをするかもしれない
cron_bot_like_followees_timeline_records:
	gcloud scheduler jobs create http like-study-records-job \
		--location=$(GCP_REGION) \
		--description="miyavinがユーザーの学習記録にいいねをする" \
		--schedule="0 0 */2 * *" \
		--uri ${BOT_LIKE_JOB_ENDPOINT} \
		--http-method=POST \
		--time-zone="UTC" \
		--project=$(GCP_PROJECT_ID) \




# studyplus-plus-DB
.PHONY: create-studyplus-plus-db-bucket push-studyplus-plus-db deploy-studyplus-plus-db

BUCKET_NAME = studyplus-plus-db

create-studyplus-plus-db-bucket:
	gcloud storage buckets create "gs://${BUCKET_NAME}" --location=$(GCP_REGION)



# push-studyplus-plus-db:
# 	docker build --platform linux/amd64 -f api/Dockerfile -t $(STUDYPLUS_PLUS_DB_IMAGE) .
# 	docker push $(STUDYPLUS_PLUS_DB_IMAGE)

# deploy-studyplus-plus-db:
# 	gcloud run deploy $(STUDYPLUS_PLUS_SERVICE) \
# 		--image $(STUDYPLUS_PLUS_DB_IMAGE) \
# 		--region $(GCP_REGION) \
# 		--project $(GCP_PROJECT_ID) \
# 		--allow-unauthenticated \
# 		--max-instances=1 \
# 		--min-instances=0 \
# 		--memory=256Mi \
# 		--timeout=30s \





# # MCPサーバー
# .PHONY: push-mcp deploy-mcp


# push-mcp:
# 	docker build -f mcp/Dockerfile -t $(MCP_IMAGE) .
# 	docker push $(MCP_IMAGE)

# deploy-mcp:
# 	gcloud run deploy $(MCP_SERVICE) \
# 		--image=$(MCP_IMAGE) \
# 		--platform=managed \
# 		--GCP_REGION=$(GCP_REGION) \
# 		--allow-unauthenticated

# mcp-all: push-mcp deploy-mcp

# # 全サービス
# .PHONY: push-all deploy-all

# push-all: push-studyplus push-mcp

# deploy-all: deploy-studyplus deploy-mcp