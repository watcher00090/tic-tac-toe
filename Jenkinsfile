@NonCPS
def getFileType(String fileName) {
  def matcher =  fileName =~ /.*\.(\w+)$/
  return matcher[0][1]
}

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
        echo 'Building the project...'
        sh "docker build -t tic-tac-toe-test:build-$BUILD_ID ."
        sh 'docker image ls'
        sh "docker volume create --driver local --opt type=ext4 --name build-$BUILD_ID-artifacts --opt device=:/data/docker-volume-store/build-$BUILD_ID-artifacts"      
      }
    }

    stage('Test') {
      steps {
        script {
          def files = findFiles(glob: 'test/*.*')
          for (int i = 0; i < files.length; i++) {
            echo "Attempting to run test ${files[i].name}"
            def fileName = "${files[i].name}"
            if (fileName != "driver.py" && getFileType(fileName).toLowerCase() == "py") {
              sh "docker run -v build-$BUILD_ID-artifacts:/home/data/ --env ARTIFACTS_DATAPATH=/home/data tic-tac-toe-test:build-$BUILD_ID 'python /home/ubuntu/test/${files[i].name}"
            }
          }
        }
      }
    }

  }
}