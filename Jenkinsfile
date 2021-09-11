pipeline {
  agent any
  options {
    timestamps()
  }
  environment {
    GIT_BRANCH = """${sh(
      returnStdout: true,
      script: 'git branch --show-current'
    ).trim()}"""
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
        env code_path = 
        script {
          String dirPath = '$WORKSPACE/tic-tac-toe_$GIT_BRANCH'
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
}