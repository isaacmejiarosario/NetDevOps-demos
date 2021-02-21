pipeline {
  agent any
  stages {
      stage('Deploy'){
      steps{
        sh 'bash $WORKSPACE/deploy-ntp.sh'
      }
    }

  }
}
