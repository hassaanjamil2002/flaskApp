pipeline {
    agent any

    environment {
        // Define environment variables (if needed)
        VENV = "venv"  // Virtual environment folder
        APP_DIR = "flaskApp"  // App directory after cloning
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                git 'https://github.com/hassaanjamil2002/flaskApp.git'
            }
        }

        stage('Set Up Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                python3 -m venv ${VENV}
                source ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                source ${VENV}/bin/activate
                pytest
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo 'Building the application...'
                // Add any specific build steps here, if applicable
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying the application...'
                sh '''
                source ${VENV}/bin/activate
                python app.py &
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            sh '''
            deactivate || true
            rm -rf ${VENV}
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}
