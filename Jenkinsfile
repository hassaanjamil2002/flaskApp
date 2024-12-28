pipeline {
    agent any

    environment {
        VENV = "venv"  // Virtual environment folder
        APP_DIR = "flaskApp"  // App directory after cloning
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/hassaanjamil2002/flaskApp.git'
            }
        }

        stage('Set Up Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                bat '''
                python -m venv %VENV%
                call %VENV%\\Scripts\\activate
                pip install -r requirements.txt
                deactivate
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                bat '''
                call %VENV%\\Scripts\\activate
                pytest
                deactivate
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
                bat '''
                call %VENV%\\Scripts\\activate
                python app.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            bat '''
            call %VENV%\\Scripts\\deactivate || echo "No active environment to deactivate"
            rmdir /s /q %VENV%
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
