pipeline {
  agent any
  stages {
      stage('Build Config Dev') {
      steps {
          sh 'bash $WORKSPACE/build-config-dev.sh'
      }
    }

      stage('Test Dev') {
      steps {
          sh 'bash $WORKSPACE/test-dev.sh'
      }
    }

      stage('Deploy Prod'){
      steps{
        sh 'bash $WORKSPACE/build-config-prod.sh'
      }
    }
  }
}
