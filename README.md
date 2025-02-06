# DeployAI: Cloud Deployment Application

DeployAI automates the deployment of applications to Azure using Terraform while leveraging LangChain for natural language input parsing. This tool streamlines the entire deployment process, it retrieves source code to configuring cloud infrastructure and deploys it to the prefered cloud service provider. 

---

## Features

- **Azure CLI Integration**: Automates cloud deployment tasks on Azure.
- **AWS CLI Integration**: Automates cloud deployment tasks on Aws.
- **LangChain Parsing**: Extracts key configuration details from natural language deployment instructions.
- **Terraform Management**: Dynamically generates and applies Terraform configurations to provision Azure Virtual Machines.
- **Repository Handling**: Supports both GitHub repository URLs and local ZIP file inputs for source code retrieval.
- **Dependency Installation**: Automatically generates a PowerShell script (`install_dependencies.ps1`) to install all necessary dependencies.

---

## Workflow

1. **Input Handling**:  
   - User provides a GitHub repository URL or a local ZIP file path along with specific deployment instructions.

2. **Code Retrieval**:  
   - The **RepositoryManager** module retrieves the source code from the specified GitHub repository or extracts it from the local ZIP file.

3. **Input Parsing**:  
   - The **langchain_parser** module processes the provided instructions to extract vital deployment parameters (e.g., application framework, cloud provider).

4. **Dependency Installation**:  
   - The **repository_analysis** module scans the codebase (e.g., checking for `requirements.txt` or `package.json`) and generates an `install_dependencies.ps1` script for installing required dependencies.

5. **Deployment**:  
   - The **deploy_app** module, in conjunction with **terraform_management.py**, uses Terraform to configure and provision an Azure VM.
   - Post-provisioning, Azure CLI deploys the application from the retrieved codebase onto the VM.

---

## Requirements

- **Azure CLI**
- **AWS CLI**
- **Terraform**
- **PowerShell**
- **LangChain**
- **Python 3.x**

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd src

