import boto3
import subprocess

# Remember to export AWS_PROFILE prior to running
# TODO: automate this via CI

def build_docker_image(image_name, dockerfile_path):
    try:
        subprocess.run(["docker", "build", "--platform=linux/amd64", "-t", image_name, "-f", dockerfile_path, "."], check=True)
        print("Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Docker image: {e}")
        raise


def push_to_ecr(image_name, repository_uri):
    ecr_client = boto3.client("ecr")
    try:
        token = ecr_client.get_authorization_token()
        registry = token['authorizationData'][0]['proxyEndpoint']
        login_cmd = subprocess.Popen(["aws", "ecr", "get-login-password"], stdout=subprocess.PIPE)
        password = login_cmd.communicate()[0].decode('utf-8').strip()

        subprocess.run(["docker", "login", "-u", "AWS", "-p", password, registry], check=True)
        subprocess.run(["docker", "tag", image_name, f"{repository_uri}:{image_name}"], check=True)
        subprocess.run(["docker", "push", f"{repository_uri}:{image_name}"], check=True)
        print(f"Image {image_name} pushed to ECR.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push image to ECR: {e}")
        raise


def main():
    image_name = "modelinference"
    dockerfile_path = "Dockerfile"
    repository_uri = "844544735981.dkr.ecr.ca-central-1.amazonaws.com/canihaveatvshowplz-staging/modelinferencerepo"

    build_docker_image(image_name, dockerfile_path)
    push_to_ecr(image_name, repository_uri)
