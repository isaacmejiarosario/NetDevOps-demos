pipeline {
  agent any
  stages {
      stage('Deploy'){
      steps{
        sh 'bash $WORKSPACE/Deploy/deploy-ntp.sh'
      }
    }

  }
}
