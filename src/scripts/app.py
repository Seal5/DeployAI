import os
from repository_manager import RepositoryManager
from langchain_parser import parse_deployment_chat
from repository_analysis import check_configurations
from deploy_app import deploy_to_vm
from langchain_parser import parse_deployment_chat

def main():
    """
    Main application entry point:
      1. Prompt user for a GitHub URL or local ZIP path and the instructions seperately.
      2. Retrieve code using RepositoryManager.
      3. Use langchain_parser to extract necessary information.
      4. Run repository_analysis to generate install_dependencies.ps1.
      5. Finally, deploy to Azure VM using Terraform via deploy_app.
    """

    # 1. Prompt for repo path and instructions
    repo_input = input("Enter a GitHub repository URL or a local '.zip' file path: ").strip()
    if not repo_input:
        print("No repository input provided. Exiting.")
        return

    instructions = input("Enter your instructions for the application: ").strip()
    if not instructions:
        print("No instructions provided (continuing without instructions).")

    # 2. Retrieve the code base into ./workspace
    manager = RepositoryManager(workspace_dir="./workspace")
    local_repo_path = manager.get_repository(repo_input)
    if not local_repo_path:
        print("Failed to retrieve repository. Exiting.")
        return

    # 3. Use langchain_parser to extract necessary information
    info = parse_deployment_chat(instructions)

    # 4. Run repository_analysis to generate install_dependencies.ps1
    check_configurations(local_repo_path)

    # 5. Deploy to Azure VM using Terraform via deploy_app.
    deploy_to_vm(local_repo_path, info)

if __name__ == "__main__":
    main()

