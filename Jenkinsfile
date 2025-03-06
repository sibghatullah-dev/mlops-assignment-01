// Jenkinsfile
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "huzi0906/legal-doc-analyzer:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies & Lint') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 .'
            }
        }
        stage('Run Tests') {
            steps {
                // Ensure tests run from the correct directory
                sh 'pip install -r app/requirements.txt'
                sh 'pip install pytest'
                sh 'pytest tests/'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
        stage('Deploy') {
            steps {
                // Deploy your Docker container to your production server
                // This could be a simple docker run command on a remote host
                echo 'Deploying the Docker container...'
            }
        }
    }
    post {
        success {
            // Send admin notification (e.g., via email)
            mail to: 'admin@example.com',
                 subject: "Deployment Success - Build ${env.BUILD_NUMBER}",
                 body: "The legal document analyzer has been successfully deployed."
        }
        failure {
            mail to: 'admin@example.com',
                 subject: "Deployment Failed - Build ${env.BUILD_NUMBER}",
                 body: "There was an error in the deployment process."
        }
    }
}
