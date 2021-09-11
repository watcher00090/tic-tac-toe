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
            import groovy.io.FileType
            def list = []
            def dir = new File(env.WORKSPACE + "/test/")
            dir.eachFileRecurse (FileType.FILES) { file ->
              list << file
            }
            for (int i = 0; i < list.length; i++) {
                if (list[i].name != "driver.py") {
                  echo "About to run test for ${list[i].name}..."
                  // sh 'docker run build-$BUILD_ID-artifacts bash -c "python "'
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