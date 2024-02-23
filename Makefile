MODEL_INFERENCE_VERSION := $(shell cat model_inference/version)
MODEL_DATA_VERSION := $(shell cat model_training/data_version)
MODEL_TRAINING_VERSION := $(shell cat model_training/training_version)

MODEL_TRAINING_TEMPLATE := model_training_template.yaml
MODEL_SERVING_TEMPLATE := model_serving_template.yaml
MODEL_TRAINING_CONFIG := model_training_samconfig.toml
MODEL_SERVING_CONFIG := model_serving_samconfig.toml

.PHONY: upload-client-staging
upload-client-staging:
	@cd client && npm run build:staging && aws s3 sync dist s3://canihaveatvshowplz-serving-staging-clientbucket

.PHONY: build-model-training-staging
build-model-training-staging:
	@$(MAKE) build-staging TEMPLATE_FILE=$(MODEL_TRAINING_TEMPLATE) CONFIG_FILE=$(MODEL_TRAINING_CONFIG)

.PHONY: deploy-model-training-staging
deploy-model-training-staging:
	@$(MAKE) deploy-staging CONFIG_FILE=$(MODEL_TRAINING_CONFIG)

.PHONY: build-model-serving-staging
build-model-serving-staging:
	@$(MAKE) build-staging TEMPLATE_FILE=$(MODEL_SERVING_TEMPLATE) CONFIG_FILE=$(MODEL_SERVING_CONFIG)

.PHONY: deploy-model-serving-staging
deploy-model-serving-staging:
	@$(MAKE) deploy-staging CONFIG_FILE=$(MODEL_SERVING_CONFIG)

.PHONY: build-staging
build-staging:
	@sam build  --cached --skip-pull-image --build-in-source --parallel -t $(TEMPLATE_FILE) --config-file $(CONFIG_FILE) --config-env staging --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION) Environment=staging

.PHONY: deploy-staging
deploy-staging:
	@sam deploy --config-file $(CONFIG_FILE) --config-env staging --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION) Environment=staging

.PHONY: build-model-training-prod
build-model-training-prod:
	@$(MAKE) build-prod TEMPLATE_FILE=$(MODEL_TRAINING_TEMPLATE) CONFIG_FILE=$(MODEL_TRAINING_CONFIG)

.PHONY: deploy-model-training-prod
deploy-model-training-prod:
	@$(MAKE) deploy-prod CONFIG_FILE=$(MODEL_TRAINING_CONFIG)

.PHONY: deploy-model-training-prod-ci
deploy-model-training-prod-ci:
	@$(MAKE) deploy-prod-ci CONFIG_FILE=$(MODEL_TRAINING_CONFIG)

.PHONY: build-model-serving-prod
build-model-serving-prod:
	@$(MAKE) build-prod TEMPLATE_FILE=$(MODEL_SERVING_TEMPLATE) CONFIG_FILE=$(MODEL_SERVING_CONFIG)

.PHONY: deploy-model-serving-prod
deploy-model-serving-prod:
	@$(MAKE) deploy-prod TEMPLATE_FILE=$(MODEL_SERVING_TEMPLATE) CONFIG_FILE=$(MODEL_SERVING_CONFIG)

.PHONY: deploy-model-serving-prod-ci
deploy-model-serving-prod-ci:
	@$(MAKE) deploy-prod-ci CONFIG_FILE=$(MODEL_SERVING_CONFIG)

.PHONY: build-prod
build-prod:
	@sam build -t $(TEMPLATE_FILE) --config-file $(CONFIG_FILE) --config-env prod --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION) Environment=prod

.PHONY: deploy-prod
deploy-prod:
	@sam deploy --config-file $(CONFIG_FILE) --config-env prod --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION) Environment=prod

.PHONY: deploy-prod-ci
deploy-prod-ci:
	@sam deploy --config-file $(CONFIG_FILE) --config-env prod --no-confirm-changeset --no-fail-on-empty-changeset --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION) Environment=prod