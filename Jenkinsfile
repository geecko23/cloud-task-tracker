pipeline{
    agent any
    stages{
        stage('Checkout Confirmation'){
            steps{
                echo "==== Verifying Workspace ===="
                pwd
                
                echo "==== Checking Required Files ===="
                test -f app.py && test -f requirements.txt && echo "All required files exist"

            }
        }


        stage{
            steps{
                sh '''
                    if [ ! -d .venv ];then
                        python3 -m venv .venv     
                    fi
                    . .venv/bin/activate
                    python -m pip install -r requirements.txt
                    cd test
                    pytest

                '''

            }
        stage('Build'){
                sh '''
                    zip deployment-${BUILD_NUMBER}.zip app.py requirements.txt
                '''
            }

            stage('Upload to S3') {
                steps {
                    sh '''
                        aws s3 cp deployment-${BUILD_NUMBER}.zip \
                            s3://cloud-task-tracker-deploy/jenkins-deployments/deployment-${BUILD_NUMBER}.zip \
                            --region us-east-1
                    '''
                }
            }
            stage('Deploy') {
                steps {
                    sshagent(credentials: ['ec2-deployment-ssh']) {
                        sh '''
                            ssh -o StrictHostKeyChecking=yes ubuntu@54.234.233.129 \
                                "FILE=deployment-${BUILD_NUMBER}.zip sudo -E /opt/cloud/deploy.sh"
                        '''
                    }
                }
            }       

        }

    }
}