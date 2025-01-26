# DeployAI
Cloud Deployment Application
This application automates the deployment of a backend application to Azure using Terraform and provides functionality to parse patient input via LangChain.

Features
Azure CLI: Used for cloud deployment tasks.
LangChain: Handles patient input parsing to extract necessary information.
Terraform: Manages cloud infrastructure configuration for Azure deployment.
Workflow
Input Handling:

User provides a GitHub repository URL or a local ZIP file path along with specific instructions.
Code Retrieval:

The RepositoryManager retrieves the source code from the specified GitHub repository or unzips the local archive.
Input Parsing:

The langchain_parser extracts relevant information based on the provided instructions.
Dependency Installation:

The repository_analysis module generates an install_dependencies.ps1 script to install all necessary dependencies.
Deployment:

The application deploys the backend to an Azure Virtual Machine using Terraform via the deploy_app module that uses the terraform_management.py file.

Requirements
Tools:

Azure CLI
Terraform
PowerShell
LangChain

To Install
cd src
python app.py


