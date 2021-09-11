pipeline {
  agent any
  stages {
    stage('Output Info') {
      parallel {
        stage('Output Info') {
          steps {
            echo "Agent = $NODE_NAME"
          }
        }

        stage('Determine tests to run') {
          steps {
            sh '''script {
  sh \'mkdir -p /tmp/build-$BUILD_ID-source-code-garbage-bag\'
  sh \'git clone https://github.com/watcher00090/tic-tac-toe /tmp/build-$BUILD_ID-source-code-garbage-bag\'
  sh \'ls -l /tmp/build-$BUILD_ID-source-code-garbage-bag\'
}'''
            }
          }

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
            String dirPath = "/home/ubuntu/tic-tac-toe/test/"
            File f = new File(dirPath);
            String[] pathnames = f.list();
            for (int i = 0; i < pathnames.length; i++) {
              if (pathnames[i] != "driver.py") {
                echo "About to run test ${i}..."
                // sh 'docker run build-$BUILD_ID-artifacts bash -c "python "'
              }
            }
          }

        }
      }

    }
    options {
      timestamps()
    }
  }