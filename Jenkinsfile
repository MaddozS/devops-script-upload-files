pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                bat "docker build -t cron-script-" + env.GIT_BRANCH + ":1.0.0-" + env.BUILD_NUMBER + " ."
            }
        }
        stage('deploy') {
            steps {
                bat "docker rm -f cron-script || 'echo no running cron-script container to remove' "
                bat "docker run -d --name cron-script -p 0.0.0.0:8090:80 cron-script-" + env.GIT_BRANCH + ":1.0.0-" + env.BUILD_NUMBER     
            }
        }
    }
    post {
        success {
            echo "Deploy success"
        }
    }
}