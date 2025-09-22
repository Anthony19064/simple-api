pipeline {
    agent any

    environment {
        VM2_SSH = "vm2-ssh-key-id"  // Credential SSH ที่สร้างไว้
        VM2_USER = "admin"
        VM2_HOST = "192.168.1.101"
        REPO_API_DIR = "~/simple-api"
        REPO_API_URL = "https://github.com/Anthony19064/simple-api.git"
        REPO_ROBOT_DIR = "~/simple-api-robot"
        REPO_ROBOT_URL = "https://github.com/Anthony19064/simple-api-Robot.git"
        IMAGE_NAME = "simple-api:latest"
    }

    stages {
        stage('Clone simple-api repo on VM2') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} \\
                        "cd ${REPO_API_DIR} && git pull || git clone ${REPO_API_URL} ${REPO_API_DIR}"
                    """
                }
            }
        }

        stage('Install requirements and run UnitTest') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        cd ${REPO_DIR}
                        python3 -m venv venv
                        ./venv/bin/pip install --upgrade pip
                        ./venv/bin/pip install -r requirements.txt
                        ./venv/bin/python -m pytest testapp.py'
                    """
                }
            }
        }

        stage('Build & Run Docker image') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        cd ${REPO_DIR}
                        docker build -t ${IMAGE_NAME} .
                        docker run --rm -p 5000:5000 ${IMAGE_NAME}'
                    """
                }
            }
        }

        stage('Clone simple-api-Robot repo on VM2') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} \\
                        "cd ${REPO_ROBOT_DIR} && git pull || git clone ${REPO_ROBOT_URL} ${REPO_ROBOT_DIR}"
                    """
                }
            }
        }

    }
}
