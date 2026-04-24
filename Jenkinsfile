pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Cal-Ryuk/edutrack.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose -f docker-compose-jenkins.yml -p edutrack-jenkins down || true'
                sh 'docker-compose -f docker-compose-jenkins.yml -p edutrack-jenkins up -d --build'
            }
        }
    }
}
