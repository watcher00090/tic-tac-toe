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
            File folder = env.WORKSPACE + "/test/"
            for (final File fileEntry : folder.listFiles()) {
              if (fileEntry.isDirectory()) {
                  listFilesForFolder(fileEntry);
              } else {
                  System.out.println(fileEntry.getName());
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