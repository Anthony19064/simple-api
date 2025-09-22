pipeline {
    agent any

    stages {
        stage('Clone simple-api on VM2') {
            steps {
                sshagent(['vm2-ssh-key-id']) {  // SSH credential ที่เก็บใน Jenkins
                    sh '''
                    ssh -o StrictHostKeyChecking=no user@192.168.1.101 "
                        cd /home/user || mkdir -p /home/user
                        cd /home/user
                        if [ -d simple-api ]; then
                            cd simple-api
                            git pull origin main
                        else
                            git clone https://github.com/Anthony19064/simple-api.git
                        fi
                    "
                    '''
                }
            }
        }
    }
}
