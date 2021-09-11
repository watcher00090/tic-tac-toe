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
        sh 'docker build -t build-$BUILD_ID:latest .'
        sh 'docker image ls'
        sh 'docker volume create --driver local --opt type=ext4 --name build-$BUILD_ID-artifacts --opt device=:/data/docker-volume-store/build-$BUILD_ID-artifacts'
      }
    }

    stage('Test') {
      steps {
        script {
          try {
            File codeDirectory = new File("${env.WORKSPACE}/test");
            File[] listOfFiles = codeDirectory.listFiles();
            for (int i = 0; i < listOfFiles.length; i++) {
              if (listOfFiles[i].isFile()) {
                if (listOfFiles[i].getName() != "driver.py") {
                  echo "About to run test for ${pathnames[i]}..."
                  // sh 'docker run build-$BUILD_ID-artifacts bash -c "python "'
                }
              }
            }
          } catch (e) {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
            String sStackTrace = sw.toString(); // stack trace as a string
            echo "${sStackTrace}"
          }
        }

      }
    }
  }
}