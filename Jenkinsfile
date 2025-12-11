pipeline {
    agent any

    environment {
        // Use your GitHub PAT credentials configured in Jenkins
        GIT_CREDENTIALS = 'github-pat'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/RajatGurjar09/ecommerce-devops.git',
                    credentialsId: "${GIT_CREDENTIALS}"
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
                // Use host's docker compose via mounted socket
                sh 'docker compose -f /var/jenkins_home/workspace/ecommerce-pipeline/docker-compose.yml up -d'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'All services built and deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}

