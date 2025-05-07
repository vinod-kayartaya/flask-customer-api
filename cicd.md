# Jenkins Pipeline Examples and Groovy Fundamentals

This guide provides various examples of Jenkins pipelines, demonstrating different concepts and approaches.

## 1. Basic Declarative Pipeline

This is a simple declarative pipeline showing the basic structure:

```groovy
pipeline {
    agent any

    environment {
        APP_NAME = 'flask-customer-api'
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Setup Python') {
            steps {
                sh """
                    # Create and activate virtual environment
                    python${env.PYTHON_VERSION} -m venv ${env.VENV_NAME}
                    . ${env.VENV_NAME}/bin/activate
                    python -m pip install --upgrade pip
                """
            }
        }

        stage('Build') {
            steps {
                sh """
                    . ${env.VENV_NAME}/bin/activate
                    echo "Building ${env.APP_NAME}..."
                    python -m pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                sh """
                    . ${env.VENV_NAME}/bin/activate
                    echo 'Running tests...'
                    python -m pytest
                """
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    . ${env.VENV_NAME}/bin/activate
                    echo 'Deploying application...'
                    echo "Deployment simulation"
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            echo 'Pipeline finished - cleaning up...'
            sh "rm -rf ${env.VENV_NAME}"
        }
    }
}
```

### Explanation:

- Uses declarative pipeline syntax with `pipeline` block
- Creates and manages a Python virtual environment
- Activates the virtual environment for each stage
- Cleans up the virtual environment in post actions
- Has dedicated setup stage for Python environment

## 2. Advanced Declarative Pipeline with Conditions

This example shows more advanced features of declarative pipelines:

```groovy
pipeline {
    agent any

    environment {
        DEPLOY_ENV = 'staging'
        CREDENTIALS = credentials('my-app-credentials')
        VENV_PATH = 'venv'
        PYTHON_VERSION = '3.9'
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    // Groovy script example
                    def config = [
                        app: 'flask-customer-api',
                        version: '1.0.0'
                    ]
                    env.APP_VERSION = config.version

                    // Create virtual environment
                    sh """
                        python${PYTHON_VERSION} -m venv ${VENV_PATH}
                        . ${VENV_PATH}/bin/activate
                        python -m pip install --upgrade pip
                    """
                }
            }
        }

        stage('Build') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    . ${VENV_PATH}/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh """
                            . ${VENV_PATH}/bin/activate
                            python -m pytest tests/unit
                        """
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh """
                            . ${VENV_PATH}/bin/activate
                            python -m pytest tests/integration
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { DEPLOY_ENV == 'staging' }
            }
            steps {
                withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
                    sh """
                        . ${VENV_PATH}/bin/activate
                        echo "Deploying to ${DEPLOY_ENV} environment..."
                        echo "Using API key: \${API_KEY}"  # The key will be masked in logs
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Successfully deployed version ${env.APP_VERSION}"
        }
        failure {
            echo "Deployment failed for version ${env.APP_VERSION}"
        }
        always {
            sh "rm -rf ${VENV_PATH}"
            cleanWs()  // Clean up workspace
        }
    }
}
```

### Explanation:

- Uses standard Jenkins agent
- Creates and manages Python virtual environment
- Shows advanced pipeline features like:
  - Conditional execution with `when`
  - Parallel test execution
  - Environment variables
  - Credential management
  - Post-build actions
- Includes proper cleanup in post actions

## 3. Scripted Pipeline with Error Handling

This example demonstrates a scripted pipeline with advanced error handling:

```groovy
node {
    def venvPath = 'venv'

    // Helper function to run commands in virtual environment
    def runInVenv = { cmd ->
        sh ". ${venvPath}/bin/activate && ${cmd}"
    }

    try {
        // Custom function definition
        def notifySlack(String message) {
            echo "Slack notification: ${message}"
        }

        // Environment setup
        def pythonVersion = '3.9'
        def appName = 'flask-customer-api'

        stage('Checkout') {
            checkout scm
        }

        stage('Setup Virtual Environment') {
            sh """
                python${pythonVersion} -m venv ${venvPath}
                . ${venvPath}/bin/activate
                python -m pip install --upgrade pip
            """
        }

        stage('Build') {
            try {
                runInVenv "pip install -r requirements.txt"
            } catch (Exception e) {
                notifySlack("Build failed: ${e.message}")
                throw e
            }
        }

        stage('Test') {
            def tests = [
                unit: 'tests/unit',
                integration: 'tests/integration'
            ]

            tests.each { type, path ->
                try {
                    runInVenv "python -m pytest ${path}"
                } catch (Exception e) {
                    notifySlack("${type} tests failed")
                    throw e
                }
            }
        }

    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        // Cleanup virtual environment
        sh "rm -rf ${venvPath}"
    }
}
```

### Explanation:

- Uses scripted pipeline syntax
- Includes helper function for virtual environment execution
- Creates virtual environment at the start
- Uses consistent virtual environment activation
- Cleans up in finally block

## 4. Shared Library Example

First, create a shared library structure:

```groovy
// vars/buildPythonApp.groovy
def call(Map config) {
    pipeline {
        agent any

        environment {
            APP_NAME = config.appName ?: 'default-app'
            PYTHON_VERSION = config.pythonVersion ?: '3.9'
            VENV_NAME = config.venvName ?: 'venv'
        }

        // Helper function for virtual environment operations
        def runInVenv = { cmd ->
            sh ". ${VENV_NAME}/bin/activate && ${cmd}"
        }

        stages {
            stage('Setup Environment') {
                steps {
                    sh """
                        python${PYTHON_VERSION} -m venv ${VENV_NAME}
                        . ${VENV_NAME}/bin/activate
                        python -m pip install --upgrade pip
                    """
                }
            }

            stage('Build') {
                steps {
                    script {
                        runInVenv "pip install -r requirements.txt"
                    }
                }
            }

            stage('Test') {
                steps {
                    script {
                        runInVenv "python -m pytest"
                    }
                }
            }
        }

        post {
            always {
                sh "rm -rf ${VENV_NAME}"
            }
        }
    }
}
```

Using the shared library in Jenkinsfile:

```groovy
@Library('my-shared-library') _

buildPythonApp(
    appName: 'flask-customer-api',
    pythonVersion: '3.9',
    venvName: 'venv'
)
```

### Explanation:

- Shows how to create reusable pipeline code with virtual environment support
- Includes helper function for virtual environment operations
- Demonstrates parameter passing including virtual environment configuration
- Handles virtual environment cleanup

## 5. Groovy Fundamentals Examples

Here are some Groovy examples commonly used in Jenkins pipelines:

```groovy
// Variables and data types
def stringVar = 'Hello'
def numberVar = 42
def listVar = ['a', 'b', 'c']
def mapVar = [name: 'John', age: 30]

// String interpolation
echo "String: ${stringVar}"

// Control structures
if (numberVar > 40) {
    echo 'Number is greater than 40'
} else {
    echo 'Number is less than or equal to 40'
}

// Loop examples
for (item in listVar) {
    echo "Item: ${item}"
}

listVar.each { item ->
    echo "Item: ${item}"
}

// Closure example
def multiply = { x, y -> x * y }
def result = multiply(6, 7)

// Function definition
def sayHello(name) {
    return "Hello, ${name}!"
}

// Exception handling
try {
    // Some risky operation
    sh 'some-command'
} catch (Exception e) {
    echo "Error: ${e.message}"
} finally {
    echo 'Cleanup'
}
```

### Explanation:

- Shows basic Groovy syntax
- Demonstrates different data types
- Illustrates control structures
- Shows closure usage
- Demonstrates function definitions
- Shows exception handling

## Best Practices

1. **Pipeline Organization**

   - Keep stages focused and single-purpose
   - Use meaningful stage names
   - Implement proper error handling
   - Include cleanup steps

2. **Code Reusability**

   - Use shared libraries for common functionality
   - Parameterize your pipelines
   - Create reusable functions

3. **Security**

   - Use credential management
   - Don't hardcode sensitive information
   - Implement proper access controls

4. **Performance**

   - Use parallel stages when possible
   - Clean up workspace after builds
   - Optimize build steps

5. **Maintenance**
   - Comment complex logic
   - Use consistent naming conventions
   - Keep pipeline code version controlled

These examples demonstrate various aspects of Jenkins pipelines, from basic concepts to advanced implementations. They can be customized based on specific project needs and requirements.
