pipeline {
    agent {
        node {
            label 'windows'
        }
    }

    environment {
        PYTHON_VERSION = '3.10'
        WORKSPACE_DIR = 'E-ComWebAutomation_AI'
        TEST_REPORTS_DIR = 'test-reports'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    triggers {
        // Run daily at midnight
        cron('0 0 * * *')
        // Run on pull requests
        pullRequest()
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    // Create and activate virtual environment
                    bat """
                        python -m venv venv
                        call venv\\Scripts\\activate
                        python -m pip install --upgrade pip
                        pip install -r ${WORKSPACE_DIR}\\requirements.txt
                    """
                }
            }
        }

        stage('Install Chrome') {
            steps {
                script {
                    // Download and install Chrome browser
                    powershell '''
                        $Path = $env:TEMP; 
                        $Installer = "chrome_installer.exe"
                        Invoke-WebRequest "http://dl.google.com/chrome/install/375.126/chrome_installer.exe" -OutFile $Path\\$Installer
                        Start-Process -FilePath $Path\\$Installer -Args "/silent /install" -Verb RunAs -Wait
                        Remove-Item $Path\\$Installer
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Create reports directory
                    bat "mkdir ${TEST_REPORTS_DIR}"

                    // Run tests with pytest
                    bat """
                        call venv\\Scripts\\activate
                        cd ${WORKSPACE_DIR}
                        pytest -v -n auto --dist=loadfile --html=${TEST_REPORTS_DIR}\\test-report.html --self-contained-html
                    """
                }
            }
            post {
                always {
                    // Archive test results and generate report
                    archiveArtifacts artifacts: "${TEST_REPORTS_DIR}/**/*", fingerprint: true
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: TEST_REPORTS_DIR,
                        reportFiles: 'test-report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
    }

    post {
        success {
            script {
                emailext(
                    subject: "Pipeline Successful: ${currentBuild.fullDisplayName}",
                    body: """
                        Pipeline execution completed successfully.
                        Check the test report for details: ${BUILD_URL}Test_Report/
                    """,
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']]
                )
            }
        }
        failure {
            script {
                emailext(
                    subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                    body: """
                        Pipeline execution failed.
                        Check the console output for details: ${BUILD_URL}console
                    """,
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']]
                )
            }
        }
        cleanup {
            // Clean workspace after build
            cleanWs()
        }
    }
}