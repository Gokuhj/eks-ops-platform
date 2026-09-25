pipeline {
    agent any

    stages {
        stage('Checkout Test') {
            steps {
                echo 'GitHub checkout successful!'
            }
        }

        stage('Environment Test') {
            steps {
                bat 'git --version'
                bat 'docker --version'
                bat 'kubectl version --client'
            }
        }
    }
}