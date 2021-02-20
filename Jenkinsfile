pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          sh 'bash $WORKSPACE/Build/basic.sh'
        
      }
    }
    stage('Deploy'){
      steps{
        sh 'bash $WORKSPACE/Deploy/deploy-ntp.sh'
      }
    }

  }
}
