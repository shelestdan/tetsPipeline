pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
    }

    environment {
        DOCKER_IMAGE = "shelestdan/my-flask-app:${env.BUILD_NUMBER}"
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
                    docker.image('python:3.11').inside("-e HOME=/tmp") {
                        sh '''
                            python -m venv venv
                            source venv/bin/activate
                            pip install --no-cache-dir -r requirements.txt
                            pytest tests/
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build(DOCKER_IMAGE)
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
                script {
                    try {
                        sh 'docker-compose down || true'  // Игнорируем ошибку, если контейнер не запущен
                        sh 'docker-compose up -d'
                        sh 'docker ps | grep my-flask-app' // Проверяем, что контейнер запущен
                    } catch (Exception e) {
                        error "Ошибка при деплое: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    sh 'docker system prune -af'
                } catch (Exception e) {
                    echo "Ошибка при очистке Docker: ${e.message}"
                }
            }
        }
    }
}
