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
      stage ("Slack notification") {	
	      slackSend baseUrl: 'https://hooks.slack.com/services/T02FTAS2SQ7/', 
	      channel: 'imejia-netdevops-demos', 
	      color: 'good', 
	      message: 'The mpls-l3vpn jenkins job has been complted..', 
	      tokenCredentialId: 'slack-netdevops-demo'
 }
  }
}
