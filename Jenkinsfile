pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                // 'checkout scm' tells Jenkins to automatically pull the code
                checkout scm
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up --build -d'
            }
        }
    }
}