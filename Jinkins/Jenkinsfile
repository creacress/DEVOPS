pipeline {
    agent any

    environment {
        CONTAINER_ID = ''
        SUM_PY_PATH = './sum.py'
        DIR_PATH = '.'
        TEST_FILE_PATH = './test_variables.txt'
        DOCKERHUB_USERNAME = credentials('dockerhub-username')
        DOCKERHUB_PASSWORD = credentials('dockerhub-password')
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
                    def output = sh(script: "docker run -dit sum-image", returnStdout: true)
                    CONTAINER_ID = output.trim()
                    echo "Container ID: ${CONTAINER_ID}"
                }
            }
        }

        stage('Test') {
            steps {
                echo '✅ Run Tests...'
                script {
                    def testLines = readFile("${TEST_FILE_PATH}").split('\n')
                    for (line in testLines) {
                        def vars = line.trim().split(' ')
                        def arg1 = vars[0]
                        def arg2 = vars[1]
                        def expectedSum = vars[2].toFloat()

                        def output = sh(script: "docker exec ${CONTAINER_ID} python sum.py ${arg1} ${arg2}", returnStdout: true)
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
                sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
                sh "docker tag sum-image ${DOCKERHUB_USERNAME}/sum-image"
                sh "docker push ${DOCKERHUB_USERNAME}/sum-image"
            }
        }
    }

    post {
        always {
            echo '🧹 Cleanup...'
            sh "docker stop ${CONTAINER_ID} || true"
            sh "docker rm ${CONTAINER_ID} || true"
        }
    }
}
