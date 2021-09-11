pipeline {
  agent any
  options { 
    timestamps() 
  }
  environment {
    TEST_NUM = '0'
  }
  stages {
    stage('Output Info') {
      steps {
        echo "Agent = $NODE_NAME" 
      }
    }
    stage('Build') {
      withEnv['TEST_NUM=$(($TEST_NUM+1))'] {
        steps {
          echo "Building the project..." 
          
          sh 'docker build -t build-$BUILD_ID-test-$TEST_NUM:latest .'
          sh "docker image ls"
        }
      }
    }
  }
}
