pipeline {
    agent any
    tools {
        jdk 'jdk17'
    }
   environment {
    SCANNER_HOME = tool 'sonar-scanner'
}
    
    stages {
        
        stage('git checkout') {
            steps {
               git branch: 'main', credentialsId: 'git-tocken', url: 'https://github.com/abhisheksali55/Ai-text-summarizer-tool.git'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                sh "trivy fs --format table -o fs.html ."
            }
        }
        stage('SonarQube Analysis') {
            steps {
               withSonarQubeEnv('sonar-server') {
                   sh '''$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Ai-text -Dsonar.projectKey=Ai-text \
                   -Dsonar.python.version=3'''
               }
            }
        }
        stage('Docker Build & Teg') {
            steps {
                script {
               withDockerRegistry(credentialsId: 'github-tocken', toolName: 'docker') {
               sh "docker build -t divyeshsali/ai-project:latest ."
               }
             }
            }
        }
        stage('Trivy image Scan') {
            steps {
                sh "trivy image --format table -o image.html divyeshsali/ai-project:latest"
            }
        }
       stage('Docker Push Image') {
            steps {
                script {
               withDockerRegistry(credentialsId: 'github-tocken', toolName: 'docker') {
               sh "docker push divyeshsali/ai-project:latest"
               }
             }
            }
        }
    }
}
