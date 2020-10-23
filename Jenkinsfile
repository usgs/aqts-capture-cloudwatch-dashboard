@Library(value='iow-ecs-pipeline@2.2.0', changelog=false) _

pipeline {
    agent {
        node {
            label 'team:iow'
        }
    }
    parameters {
        choice(choices: ['DEV', 'TEST', 'QA', 'PROD-EXTERNAL'], description: 'Deploy Stage (i.e. tier)', name: 'DEPLOY_STAGE')
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages {
        stage('Run python script to build dashboard') {
            agent {
                dockerfile {
                    label 'team:iow'
                }
            }
            steps {
                script {
                    // By default, jenkins has access to prod account/vpc environment variables.
                    // If deploying to dev account/vpc, we need to change these default values.
                    if ("${params.DEPLOY_STAGE}" == 'DEV') {
                        def secretsString = sh(script: '/usr/local/bin/aws ssm get-parameter --name "/aws/reference/secretsmanager/IOW_AWS" --query "Parameter.Value" --with-decryption --output text --region "us-west-2"', returnStdout: true).trim()
                        def secretsJson = readJSON text: secretsString
                        def iowDevAccountNumber = secretsJson.accountNumber
                        def devAccountRoleName = secretsJson.roleName

                        def assumeRoleName = "arn:aws:iam::$iowDevAccountNumber:role/$devAccountRoleName"
                        def assumeRoleResp = sh(script: "/usr/local/bin/aws sts assume-role --role-arn $assumeRoleName --role-session-name expt-session --duration-seconds 3600", returnStdout: true).trim()
                        def roleJson = readJSON text: assumeRoleResp
                        env.AWS_ACCESS_KEY_ID = roleJson.Credentials.AccessKeyId
                        env.AWS_SECRET_ACCESS_KEY = roleJson.Credentials.SecretAccessKey
                        env.AWS_SESSION_TOKEN = roleJson.Credentials.SessionToken
                    }
                    // Python/boto3 entrypoint to create the dashboard
                    sh '''
                        python --version
                        python3 -m pip --version
                        ls -al
                        pip install -r requirements.txt
                        python dashboard.py
                    '''
                }
            }
        }
        stage('Set build description') {
            steps {
                script {
                    currentBuild.description = "Created dashboard on ${env.DEPLOY_STAGE} tier"
                }
            }
        }
    }
    post {
        always {
            script {
                pipelineUtils.cleanWorkspace()
            }
        }
        failure {
            script {
                pipelineUtils.sendEmailNotification(
                    to: 'ssoper@contractor.usgs.gov',
                    attachLog: true
                )
            }
        }
    }
}
