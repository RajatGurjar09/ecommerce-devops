pipeline {
    agent any

    stages {
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
                sh 'docker compose up -d'
            }
        }
    }
}
