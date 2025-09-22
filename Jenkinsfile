pipeline {
    agent any

    environment {
        VM2_SSH = "vm2-ssh-key-id"  // Credential SSH ที่สร้างไว้
        VM2_USER = "admin"
        VM2_HOST = "192.168.1.101"
        REPO_DIR = "~/simple-api"
        REPO_URL = "https://github.com/Anthony19064/simple-api.git"
    }

    triggers {
        // Trigger pipeline จาก GitHub webhook
        githubPush()
    }

    stages {
        stage('Checkout main branch') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} \\
                        "if [ -d ${REPO_DIR} ]; then cd ${REPO_DIR} && git checkout main && git pull; else git clone -b main ${REPO_URL} ${REPO_DIR}; fi"
                    """
                }
            }
        }

        stage('Setup Python and run tests') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        cd ${REPO_DIR}
                        if [ ! -d venv ]; then
                            python3 -m venv venv
                        fi
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install pytest
                        python -m pytest testapp.py
                        deactivate
                        '
                    """
                }
            }
        }
    }
}
