pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                bat 'venv\\Scripts\\python Experiment7.py'
            }
        }
    }
}