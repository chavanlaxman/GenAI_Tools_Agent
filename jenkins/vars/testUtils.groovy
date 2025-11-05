// vars/testUtils.groovy

/**
 * Set up Python virtual environment and install dependencies
 */
def setupPythonEnv(String pythonVersion, String requirementsPath) {
    bat """
        python -m venv venv
        call venv\\Scripts\\activate
        python -m pip install --upgrade pip
        pip install -r ${requirementsPath}
    """
}

/**
 * Install Chrome browser on Windows
 */
def installChrome() {
    powershell '''
        $Path = $env:TEMP
        $Installer = "chrome_installer.exe"
        Invoke-WebRequest "http://dl.google.com/chrome/install/375.126/chrome_installer.exe" -OutFile $Path\\$Installer
        Start-Process -FilePath $Path\\$Installer -Args "/silent /install" -Verb RunAs -Wait
        Remove-Item $Path\\$Installer
    '''
}

/**
 * Run Pytest with HTML report generation
 */
def runTests(String workspaceDir, String reportsDir) {
    // Create reports directory if it doesn't exist
    bat "mkdir ${reportsDir}"
    
    // Run tests
    bat """
        call venv\\Scripts\\activate
        cd ${workspaceDir}
        pytest -v --html=${reportsDir}\\test-report.html --self-contained-html
    """
}

/**
 * Archive and publish test results
 */
def publishTestResults(String reportsDir) {
    // Archive artifacts
    archiveArtifacts artifacts: "${reportsDir}/**/*", fingerprint: true
    
    // Publish HTML report
    publishHTML([
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: reportsDir,
        reportFiles: 'test-report.html',
        reportName: 'Test Report'
    ])
}

/**
 * Send email notification
 */
def sendNotification(String status, String subject, String body) {
    emailext(
        subject: subject,
        body: body,
        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}

/**
 * Execute parallel tests with multiple configurations
 */
def runParallelTests(Map config) {
    def parallelStages = [:]
    
    config.browsers.each { browser ->
        config.environments.each { env ->
            def stageName = "Test_${browser}_${env}"
            parallelStages[stageName] = {
                stage(stageName) {
                    runTests(config.workspaceDir, "${config.reportsDir}/${stageName}")
                }
            }
        }
    }
    
    parallel parallelStages
}

/**
 * Check system requirements
 */
def checkRequirements() {
    // Check Python version
    def pythonVersion = bat(
        script: 'python --version',
        returnStdout: true
    ).trim()
    
    // Check available disk space
    def diskSpace = powershell(
        script: '(Get-PSDrive C).Free / 1GB',
        returnStdout: true
    ).trim()
    
    return [
        pythonVersion: pythonVersion,
        diskSpaceGB: diskSpace
    ]
}

/**
 * Generate test execution summary
 */
def generateTestSummary(String reportsDir) {
    def summary = [:]
    
    // Parse pytest results
    def testResults = readFile("${reportsDir}/test-report.html")
    
    // Extract test counts (simplified example)
    summary.total = (testResults =~ /\d+ tests/).findAll().size()
    summary.passed = (testResults =~ /class="passed"/).findAll().size()
    summary.failed = (testResults =~ /class="failed"/).findAll().size()
    
    return summary
}

return this