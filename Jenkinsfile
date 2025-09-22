pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "myusername" // เปลี่ยนเป็น Docker Hub หรือ registry ของคุณ
        IMAGE_NAME = "simple-api"
    }

    stages {
        stage('Clone simple-api') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Anthony19064/simple-api.git',
                credentialsId: 'Anthony19064'

            }
        }

        stage('Run Unit Test') {
            steps {
                sh 'docker run --rm -v $PWD:/app -w /app python:3.11 bash -c "pip install -r requirements.txt && pytest"'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:latest ."
            }
        }

        stage('Run Container for Robot Test') {
            steps {
                sh "docker run -d --name simple-api-test -p 5000:5000 $DOCKER_REGISTRY/$IMAGE_NAME:latest"
            }
        }

        stage('Clone simple-api-robot') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/simple-api-robot.git'
            }
        }

        // stage('Run Robot Test') {
        //     steps {
        //         sh 'robot tests/'  // สมมติไฟล์ Robot อยู่ใน folder tests/
        //     }
        // }

        stage('Push Image to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh "docker push $DOCKER_REGISTRY/$IMAGE_NAME:latest"
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker rm -f simple-api-test || true'
            }
        }
    }
}
