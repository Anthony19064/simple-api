pipeline {
    agent any

    environment {
        VM2_SSH = "vm2-ssh-key-id"  // Credential SSH ที่สร้างไว้
        VM2_USER = "admin"
        VM2_HOST = "192.168.1.101"
        REPO_DIR = "~/simple-api"
        REPO_URL = "https://github.com/Anthony19064/simple-api.git"
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
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} \\
                        "cd ${REPO_DIR} && pip3 install -r requirements.txt && python3 testapp.py"
                    """
                }
            }
        }
    }
}
