pipeline {
  agent any
  stages {
    stage('Build Config Dev') {
      when {
        expression {
          BRANCH_NAME == "dev"
        }
      }
      steps {
        sh 'bash $WORKSPACE/build-config-dev.sh'
          }
        }
    stage ("Dev Test") {	
      when {
        expression {
          BRANCH_NAME == "dev"
            }
        }
      steps {
        build 'mpls-l3vpn-pyats-test'
        }
    }
    stage('Release Config'){
      when {
        expression {
          BRANCH_NAME == "master"
            }
        }
      steps{
        sh 'bash $WORKSPACE/build-config-prod.sh'
      }
    }
    stage ("Slack notification") {
      when {
        expression {
          BRANCH_NAME == "master"
            }
        }
      steps{
	    slackSend baseUrl: 'https://hooks.slack.com/services/T02FTAS2SQ7/', 
	    channel: 'imejia-netdevops-demos', 
	    color: 'good', 
	    message: 'The mpls-l3vpn jenkins job has been complted..', 
	    tokenCredentialId: 'slack-netdevops-demo'
     }
   }
  }
}
