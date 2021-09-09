pipeline {
  agent any
  stages {
    stage('Output Info') {
      steps {
        echo "Agent = $NODE_NAME" 
      }
    }
    stage('Build') {
      steps {
        echo "Building the project..." 
      }
    }
  }
}
