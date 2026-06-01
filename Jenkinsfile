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
                sh 'docker compose -f docker-compose-jenkins.yml -p edutrack-jenkins down || true'
                sh 'docker compose -f docker-compose-jenkins.yml -p edutrack-jenkins up -d --build'
                sh 'sleep 5'
            }
        }
        stage('Test') {
            steps {
                sh 'docker build -t edutrack-tests ./tests'
                sh '''
                    docker run --rm \
                        --network edutrack-jenkins_default \
                        -e BASE_URL=http://edutrack-jenkins:3000 \
                        edutrack-tests 2>&1 | tee test-results.txt
                '''
            }
            post {
                always {
                    emailext(
                        to: "${env.CHANGE_AUTHOR_EMAIL ?: 'qasimalik@gmail.com'}",
                        subject: "EduTrack Test Results - Build #${env.BUILD_NUMBER}",
                        body: """
Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}

${readFile('test-results.txt')}

Build URL: ${env.BUILD_URL}
                        """,
                        attachLog: true
                    )
                }
            }
        }
    }
}
