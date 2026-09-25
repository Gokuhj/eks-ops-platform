pipeline {
    agent any

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