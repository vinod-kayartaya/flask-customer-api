# Jenkins Automation Guide for Flask Customer API

This guide will help you set up Jenkins for automating the build and deployment of the Flask Customer API application.

## Prerequisites

1. Jenkins server installed (version 2.x or higher)
2. Docker installed on the Jenkins server
3. Python 3.9 installed on the Jenkins server
4. Access to Docker Hub account

## Required Jenkins Plugins

Install the following plugins from "Manage Jenkins" > "Manage Plugins" > "Available":

1. **Docker Pipeline** - For Docker operations within pipeline

   - Plugin ID: docker-workflow
   - Provides Docker pipeline steps

2. **Credentials Plugin** - For managing credentials

   - Plugin ID: credentials
   - Already included in Jenkins

3. **Pipeline** - For running pipeline scripts

   - Plugin ID: workflow-aggregator
   - Core pipeline functionality

4. **Git** - For source code management
   - Plugin ID: git
   - Required for checking out code

## Jenkins Configuration Steps

### 1. Install Required Plugins

1. Navigate to "Manage Jenkins" > "Manage Plugins"
2. Go to "Available" tab
3. Search and select the required plugins
4. Click "Install without restart"
5. Check "Restart Jenkins when installation is complete"

### 2. Configure Docker Hub Credentials

1. Go to "Manage Jenkins" > "Manage Credentials"
2. Click on "Jenkins" store
3. Click "Global credentials"
4. Click "Add Credentials"
5. Fill in the following:
   - Kind: Username with password
   - Scope: Global
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password or access token
   - ID: docker-hub-credentials
   - Description: Docker Hub Credentials

### 3. Configure Python Environment

Ensure Python 3.9 is available on the Jenkins server:

```bash
# Install Python 3.9 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv

# Verify installation
python3.9 --version
```

### 4. Configure Docker Permissions

Give Jenkins user permission to use Docker:

```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins service
sudo systemctl restart jenkins
```

## Creating the Pipeline

1. Click "New Item" on Jenkins dashboard
2. Enter a name (e.g., "flask-customer-api")
3. Select "Pipeline"
4. Click "OK"
5. In the configuration:
   - Under "Pipeline":
     - Definition: Pipeline script from SCM
     - SCM: Git
     - Repository URL: Your repository URL
     - Branch Specifier: \*/main
     - Script Path: Jenkinsfile.ex2

## Pipeline Customization

Modify the following variables in `Jenkinsfile.ex2`:

1. Update Docker image name:

```groovy
DOCKER_IMAGE = 'your-dockerhub-username/flask-customer-api'
```

2. Adjust integration test endpoint if needed:

```groovy
sh 'curl -f http://localhost:5000/health || exit 1'
```

## Security Considerations

1. **Docker Hub Credentials**:

   - Use access tokens instead of password
   - Regularly rotate access tokens
   - Use minimal required permissions

2. **Jenkins Security**:
   - Enable Jenkins security
   - Use HTTPS
   - Regularly update plugins
   - Implement proper access control

## Troubleshooting

### Common Issues and Solutions

1. **Docker Permission Issues**:

```bash
# Check docker group membership
groups jenkins

# Verify docker socket permissions
ls -l /var/run/docker.sock
```

2. **Python Virtual Environment Issues**:

```bash
# Check Python installation
which python3.9

# Verify venv module
python3.9 -m venv --help
```

3. **Pipeline Failures**:
   - Check Jenkins logs
   - Verify Docker Hub credentials
   - Ensure network connectivity
   - Check disk space

### Health Checks

1. **Docker Health**:

```bash
# Test Docker functionality
docker info
docker ps
```

2. **Python Health**:

```bash
# Test Python installation
python3.9 --version
pip --version
```

## Best Practices

1. **Pipeline Management**:

   - Use version control for pipeline code
   - Document all customizations
   - Implement proper error handling
   - Clean up resources after builds

2. **Security**:

   - Regular security updates
   - Proper credential management
   - Limited permissions
   - Audit logging

3. **Maintenance**:
   - Regular plugin updates
   - Backup Jenkins configuration
   - Monitor disk space
   - Review build logs

## Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Docker Pipeline Plugin Documentation](https://plugins.jenkins.io/docker-workflow/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
