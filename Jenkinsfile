pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: params.BRANCH, url: 'https://github.com/shelestdan/tetsPipeline.git'
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image('python:3.11').inside {
                        sh 'pip install -r requirements.txt'
                        sh 'pytest tests/'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("shelestdan/my-flask-app:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-cred') {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker system prune -af'  // Очистка Docker
        }
        success {
            slackSend channel: '#devops', message: "Сборка #${env.BUILD_NUMBER} успешна! 🎉"
        }
        failure {
            slackSend channel: '#devops', message: "Сборка #${env.BUILD_NUMBER} провалена! 🔥"
        }
    }
}