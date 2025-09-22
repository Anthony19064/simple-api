pipeline {
    agent any

    environment {
        VM2_SSH = "vm2-ssh-key-id"  // Credential SSH ที่สร้างไว้
        VM2_USER = "admin"
        VM2_HOST = "192.168.1.101"
        REPO_DIR = "~/simple-api"
        REPO_URL = "https://github.com/Anthony19064/simple-api.git"
        IMAGE_NAME = "simple-api:latest"
    }

    stages {
        stage('Clone repo on VM2') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} \\
                        "cd ${REPO_DIR} && git pull || git clone ${REPO_URL} ${REPO_DIR}"
                    """
                }
            }
        }

        stage('Install requirements and run test') {
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

        stage('Build Docker image') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        cd ${REPO_DIR}
                        sudo docker build -t ${IMAGE_NAME} .'
                    """
                }
            }
        }

        stage('Run container') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        sudo docker run --rm ${IMAGE_NAME}'
                    """
                }
            }
        }
    }
}
