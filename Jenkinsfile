pipeline {
    agent any

    environment {
        VM2_SSH = "vm2-ssh-key-id"  // Credential SSH ที่สร้างไว้
        VM2_USER = "admin"
        VM2_HOST = "192.168.1.101"
        VM3_SSH = "vm3-ssh-key-id"
        VM3_USER = "admin"
        VM3_HOST = "192.168.1.102"
        REPO_API_DIR = "~/simple-api"
        REPO_API_URL = "https://github.com/Anthony19064/simple-api.git"
        REPO_ROBOT_DIR = "~/simple-api-robot"
        REPO_ROBOT_URL = "https://github.com/Anthony19064/simple-api-Robot.git"
        IMAGE_NAME = "simple-api:latest"
        GITHUB_USER = "Anthony19064"
        GITHUB_USER_LOWER = "anthony19064"  // เพิ่มตัวแปรสำหรับ lowercase
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
                        cd ${REPO_API_DIR}
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
                        cd ${REPO_API_DIR}
                        docker build -t ${IMAGE_NAME} .
                        docker rm -f simple-api || true
                        docker run -d --rm --name simple-api -p 5000:5000 ${IMAGE_NAME}'
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

        stage('Run Robot Tests') {
            steps {
                sshagent([VM2_SSH]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM2_USER}@${VM2_HOST} '
                        set -e
                        cd ${REPO_ROBOT_DIR}
                        python3 -m venv venv
                        ./venv/bin/pip install --upgrade pip
                        ./venv/bin/pip install -r requirements.txt
                        ./venv/bin/robot --outputdir reports ~/simple-api-robot/testPlush.robot'
                    """
                }
            }
        }

        stage('Push Docker image to GHCR') {
            steps {
                sshagent([VM2_SSH]) {
                    withCredentials([string(credentialsId: 'GHCR_TOKEN', variable: 'GHCR_TOKEN')]) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no ''' + VM2_USER + '''@''' + VM2_HOST + ''' '
                            set -e
                            echo "''' + GHCR_TOKEN + '''" | docker login ghcr.io -u ''' + GITHUB_USER + ''' --password-stdin
                            docker tag ''' + IMAGE_NAME + ''' ghcr.io/''' + GITHUB_USER_LOWER + '''/simple-api:latest
                            docker push ghcr.io/''' + GITHUB_USER_LOWER + '''/simple-api:latest
                            '
                        '''
                    }
                }
            }
        }

        stage('Deploy to VM3') {
            steps {
                sshagent([VM3_SSH]) {
                    withCredentials([string(credentialsId: 'GHCR_TOKEN', variable: 'GHCR_TOKEN')]) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no ''' + VM3_USER + '''@''' + VM3_HOST + ''' '
                            set -e
                            echo "Logging into GitHub Container Registry..."
                            echo "''' + GHCR_TOKEN + '''" | docker login ghcr.io -u ''' + GITHUB_USER + ''' --password-stdin
                            
                            echo "Stopping existing container if running..."
                            docker stop simple-api-prod || echo "No existing container to stop"
                            docker rm simple-api-prod || echo "No existing container to remove"
                            
                            echo "Pulling latest image..."
                            docker pull ghcr.io/''' + GITHUB_USER_LOWER + '''/simple-api:latest
                            
                            echo "Starting new container..."
                            docker run -d --name simple-api-prod --restart unless-stopped -p 5000:5000 ghcr.io/''' + GITHUB_USER_LOWER + '''/simple-api:latest
                            
                            echo "Verifying deployment..."
                            sleep 5
                            curl -f http://localhost:5000/plus/2/3 || echo "Health check failed"
                            
                            echo "Deployment to VM3 completed!"
                            '
                        '''
                    }
                }
            }
        }

    }
}