pipeline {
    agent any
    stages {
        stage('Clone repo on VM2') {
            steps {
                sshagent(['Anthony19064']) {
                    sh 'ssh admin@192.168.1.101 "cd ~/simple-api || git clone https://github.com/Anthony19064/simple-api.git"'
                }
            }
        }
    }
}
