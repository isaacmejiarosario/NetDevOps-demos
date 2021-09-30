pipeline {
  agent any
  stages {
      stage('Build Config Dev') {
      steps {
          sh 'bash $WORKSPACE/build-config-dev.sh'
      }
    }

     stage ("Dev Test") {	
            steps {
                build 'mpls-l3vpn-pyats-test'
            }
        }
      stage('Deploy Prod'){
      steps{
        sh 'bash $WORKSPACE/build-config-prod.sh'
      }
    }
  }
}
