pipeline {
    agent any

    environment {
        SUM_PY_PATH = './sum.py'
        DIR_PATH = '.'
        TEST_FILE_PATH = './test_variables.txt'
    }

    stages {
        stage('Build') {
            steps {
                echo '🔨 Build Docker image...'
                sh "docker build -t sum-image ${DIR_PATH}"
            }
        }

        stage('Run') {
            steps {
                echo '🚀 Run Docker container...'
                script {
                    // CONTAINER_ID déclaré ici, accessible partout
                    env.CONTAINER_ID = sh(script: "docker run -dit sum-image", returnStdout: true).trim()
                    echo "Container ID: ${env.CONTAINER_ID}"
                }
            }
        }

        stage('Test') {
            steps {
                echo '✅ Run Tests...'
                script {
                    def testLines = readFile("${env.TEST_FILE_PATH}").split('\n')
                    for (line in testLines) {
                        def vars = line.trim().split(' ')
                        def arg1 = vars[0]
                        def arg2 = vars[1]
                        def expectedSum = vars[2].toFloat()

                        def output = sh(script: "docker exec ${env.CONTAINER_ID} python sum.py ${arg1} ${arg2}", returnStdout: true)
                        def result = output.split('\n')[-1].trim().toFloat()

                        if (result == expectedSum) {
                            echo "✅ Test OK: ${arg1} + ${arg2} = ${expectedSum}"
                        } else {
                            error "❌ Test FAIL: ${arg1} + ${arg2} != ${result}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '📦 Push to DockerHub...'
                withCredentials([
                    usernamePassword(credentialsId: 'dockerhub-username', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')
                ]) {
                    sh "docker login -u $USERNAME -p $PASSWORD"
                    sh "docker tag sum-image $USERNAME/sum-image"
                    sh "docker push $USERNAME/sum-image"
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleanup...'
            sh "docker stop ${env.CONTAINER_ID} || true"
            sh "docker rm ${env.CONTAINER_ID} || true"
        }
    }
}
