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

        stage('Verify Docker Image') {
            steps {
                bat 'docker images devops-app'
            }
        }
    }

    post {
        success {
            echo 'Docker image built successfully!'
        }

        failure {
            echo 'Docker build failed!'
        }
    }
}