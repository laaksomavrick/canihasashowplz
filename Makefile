.PHONY: build-staging
build-staging:
	@sam build --cached --skip-pull-image --build-in-source --parallel -t template.yaml --config-env staging

.PHONY: build-prod
build-prod:
	@sam build -t template.yaml -config-env prod

.PHONY: deploy-staging
deploy-staging:
	@sam deploy --config-env staging --resolve-image-repos

.PHONY: deploy-prod
deploy-prod:
	@sam deploy --config-env prod --resolve-image-repos