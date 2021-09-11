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
      steps {
        environment {
            TEST_NUM = """${sh(
                returnStdout: true,
                script: 'echo $(($TEST_NUM+1))'
            ).trim()}""" 
        }

        echo "Building the project..." 
        
        sh "docker build -t build-$BUILD_ID-test-$TEST_NUM:latest ."
        sh "docker image ls"
      }
    }
  }
}
