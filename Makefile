MODEL_INFERENCE_VERSION := $(shell cat model_inference/version)
MODEL_DATA_VERSION := $(shell cat model_training/data_version)
MODEL_TRAINING_VERSION := $(shell cat model_training/training_version)

.PHONY: build-staging
build-staging:
	@sam build --cached --skip-pull-image --build-in-source --parallel -t template.yaml --config-env staging --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION)

.PHONY: build-prod
build-prod:
	@sam build -t template.yaml --config-env prod --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION)

.PHONY: deploy-staging
deploy-staging:
	@sam deploy --config-env staging --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION)

.PHONY: deploy-prod
deploy-prod:
	@sam deploy --config-env prod --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION)

.PHONY: deploy-prod-ci
deploy-prod-ci:
	@sam deploy --config-env prod --no-confirm-changeset --no-fail-on-empty-changeset --resolve-image-repos --parameter-overrides ModelInferenceVersion=$(MODEL_INFERENCE_VERSION) ModelDataVersion=$(MODEL_DATA_VERSION) ModelTrainingVersion=$(MODEL_TRAINING_VERSION)