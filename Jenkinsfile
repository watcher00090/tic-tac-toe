pipeline {
  agent any
  options { 
    timestamps() 
  }
  stages {
    stage('Output Info') {
      steps {
        echo "Agent = $NODE_NAME" 
      }
    }
    stage('Build') {
      steps {
        echo "Building the project..." 
        
        sh 'docker build -t build-$BUILD_ID:latest .'
        sh 'docker image ls'
      }
    }
  }
}
