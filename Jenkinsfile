pipeline {
    agent any
    stages {
        stage('Clone repo on VM2') {
            steps {
                sshagent(['vm2-ssh-key-id']) {
                    sh 'ssh admin@192.168.1.101 "cd ~/simple-api || git clone https://github.com/Anthony19064/simple-api.git"'
                }
            }
        }
    }
}
