pipeline {
  agent any
  stages {
      stage('Build Config Dev') {
      steps {
          sh 'bash $WORKSPACE/build-config.sh'
      }
    }

      stage('Test Dev') {
      steps {
          sh 'bash $WORKSPACE/Test/mpls_l3vpn_easypy_test.py'
      }
    }

      stage('Deploy Prod'){
      steps{
        sh 'bash $WORKSPACE/mpls_l3vpn_config.py'
      }
    }
  }
}
