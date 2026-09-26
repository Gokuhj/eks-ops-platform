pipeline {
    agent any

     environment {
        MINIKUBE_HOME = 'C:\\Users\\user'
        KUBECONFIG = 'C:\\Users\\user\\.kube\\config'

        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'devops-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code checked out successfully'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    bat 'docker build -t devops-app:jenkins .'
                }
            }
        }

        stage('Push Image to ECR') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'aws-ecr-credentials',
                usernameVariable: 'AWS_ACCESS_KEY_ID',
                passwordVariable: 'AWS_SECRET_ACCESS_KEY'
            )
        ]) {
            script {
                bat '''
                for /f %%i in ('aws sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i

                aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com

                docker tag devops-app:jenkins %ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%ECR_REPOSITORY%:latest

                docker push %ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%ECR_REPOSITORY%:latest
                '''
            }
        }
    }
}

        stage('Load Image into Minikube') {
            steps {
                bat 'minikube image load devops-app:jenkins'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl set image deployment/devops-app devops-app=devops-app:jenkins'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl rollout status deployment/devops-app --timeout=120s'
                bat 'kubectl get pods'
                bat 'kubectl get svc'
            }
        }
    }

    post {
        success {
            echo 'CI/CD deployment successful!'
        }

        failure {
            echo 'CI/CD deployment failed!'
        }
    }
}