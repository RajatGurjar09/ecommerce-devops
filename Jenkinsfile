pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/RajatGurjar09/ecommerce-devops.git', credentialsId: 'github-pat'
            }
        }

        stage('Build Product Service') {
            steps {
                dir('source-code/product-service') {
                    sh 'docker build -t product-service:latest .'
                }
            }
        }

        stage('Build Cart Service') {
            steps {
                dir('source-code/cart-service') {
                    sh 'docker build -t cart-service:latest .'
                }
            }
        }

        stage('Build Order Service') {
            steps {
                dir('source-code/order-service') {
                    sh 'docker build -t order-service:latest .'
                }
            }
        }

        stage('Deploy Services') {
            steps {
                sh '''
                # Stop and remove any existing containers for this project
                docker-compose -f /var/jenkins_home/workspace/ecommerce-pipeline/docker-compose.yml down

                # Start all services, rebuild images if needed
                docker-compose -f /var/jenkins_home/workspace/ecommerce-pipeline/docker-compose.yml up -d --build
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}

