# canihaveashowplz

Application and model-training code to create `canihaveashowplz`.

Notebook exploration and web scraping code can be found in [this repo](https://github.com/laaksomavrick/tv-show-recommender-exploration).

## Architecture

Stage 1:

```mermaid
flowchart

    Lambda(Lambda function)
    ECR(Container registry)
    APIGW(Api Gateway)
    DynamoDB(DynamoDB)
    Client(Client SPA)


    Client --> APIGW
    APIGW --> Client

    APIGW -->|Request| Lambda
    Lambda -->|Response| APIGW
    ECR -->|Pulls| Lambda

    Lambda -->|Writes new data| DynamoDB
    Lambda -->|Reads existing data| DynamoDB
```

Stage 2:

```mermaid
flowchart

    Lambda(Lambda function)
    ECR(Container registry)
    APIGW(Api Gateway)
    DynamoDB(DynamoDB)
    S3(S3)
    Client(Client SPA)
    Cloudwatch(Cloudwatch Event)


    SageMakerEndpoint(SageMaker Serverless Model Endpoint)
    SageMaker(SageMaker retraining)

    Client --> APIGW
    APIGW --> Client

    APIGW -->|Request| Lambda
    Lambda -->|Response| APIGW
    ECR -->|Pulls| Lambda

    Lambda -->|Writes new data| DynamoDB
    Lambda -->|Reads existing data| DynamoDB
    Lambda -->|Delegates model inference| SageMakerEndpoint

    DynamoDB -->|Exports data| S3

    S3 -->|Pulls in data| SageMaker
    SageMaker -->|Deploys new model| SageMakerEndpoint

    Cloudwatch -->|Triggers| SageMaker
```