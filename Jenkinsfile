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
        sh "docker volume create --name build-$BUILD_ID-artifacts"
        script {
          env.VOLUME_MOUNT_PATH = sh(
            returnStdout: true,
            script: "docker volume inspect build-$BUILD_ID-artifacts | jq '.[0] | .Mountpoint' | sed -e 's/^\"//' -e 's/\"\$//'"
          ).trim()      
        }
        echo "Docker volume data path = ${VOLUME_MOUNT_PATH}"
      }
    }

    stage('Test') {
      steps {
        script {
          def files = findFiles(glob: 'test/*.*')
          for (int i = 0; i < files.length; i++) {
            def fileName = "${files[i].name}"
            if (fileName != "driver.py" && getFileType(fileName).toLowerCase() == "py") {
              echo "Attempting to run test ${files[i].name}"
              script {
                env.CONTAINER_ID = sh(
                  returnStdout: true,
                  script: "docker run -d -v build-$BUILD_ID-artifacts:/home/data/ --env ARTIFACTS_DATAPATH=/home/data tic-tac-toe-test:build-$BUILD_ID python /home/tic-tac-toe/test/${files[i].name}"
                )
              }
              sh "docker logs -f $CONTAINER_ID"
            }
          }
        }
      }
    }

  }
}