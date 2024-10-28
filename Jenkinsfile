pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('fastapi-app')
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        docker.image('fastapi-app').push('latest')
                    }
                    sh '''
                        docker stop fastapi-app || true
                        docker rm fastapi-app || true
                        docker run -d --name fastapi-app -p 8000:8000 fastapi-app:latest
                    '''
                }
            }
        }
    }
}
