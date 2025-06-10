# 変数定義
GCP_PROJECT_ID = studyplus-plus
GCP_REGION = asia-northeast1
REPO_NAME = studyplus-plus

# サービス定義
STUDYPLUS_SERVICE = studyplus-api
STUDYPLUS_IMAGE = $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(REPO_NAME)/$(STUDYPLUS_SERVICE)
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

push-studyplus:
	docker build -f studyplus/Dockerfile -t $(STUDYPLUS_IMAGE) .
	docker push $(STUDYPLUS_IMAGE)

deploy-studyplus:
	gcloud run deploy $(STUDYPLUS_SERVICE) \
		--image $(STUDYPLUS_IMAGE) \
		--region $(GCP_REGION) \
		--project $(GCP_PROJECT_ID) \
		--allow-unauthenticated \

studyplus-all: push-studyplus deploy-studyplus

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