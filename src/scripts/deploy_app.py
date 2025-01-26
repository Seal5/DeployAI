import os
import shutil
import subprocess
from terraform_manager import generate_terraform_config, deploy_with_terraform

def zip_application(source_dir: str) -> str:
    """Zips the application files using the folder name as the zip file name."""
    base_name = os.path.basename(os.path.normpath(source_dir))
    shutil.make_archive(base_name, 'zip', source_dir)
    return f"{base_name}.zip"

def deploy_to_vm(source_dir: str, vm_details: dict) -> bool:
    """Deploy application to Azure VM using Azure CLI."""
    try:
        # 1. First provision the VM using Terraform
        print("Provisioning VM with Terraform...")
        generate_terraform_config(vm_details)
        deploy_with_terraform()

        # 2. Zip the application
        print("Zipping application...")
        zip_file = zip_application(source_dir)

        # 3. Upload the zip file to VM
        print(f"Uploading {zip_file} to VM...")
        subprocess.run([
            "az", "vm", "run-command", "invoke",
            "--command-id", "RunPowerShellScript",
            "--name", vm_details.get('vm_name') or 'default-vm-name',
            "--resource-group", vm_details.get('resource_group_name') or 'default-resource-group',
            "--scripts", f"""
                $source = '{os.path.abspath(zip_file)}'
                $dest = 'C:\\app\\{zip_file}'
                New-Item -ItemType Directory -Force -Path 'C:\\app'
                Invoke-WebRequest -Uri $source -OutFile $dest
            """
        ], check=True)

        # 4. Extract the application and run the script located in /scripts
        print("Extracting application and running script...")
        subprocess.run([
            "az", "vm", "run-command", "invoke",
            "--command-id", "RunPowerShellScript",
            "--name", vm_details.get('vm_name') or 'default-vm-name',
            "--resource-group", vm_details.get('resource_group_name') or 'default-resource-group',
            "--scripts", f"""
                Set-Location -Path 'C:\\app'
                Expand-Archive -Path '{zip_file}' -DestinationPath '.'
                .\\scripts\\install_dependencies.ps1 
            """
        ], check=True)

        print("Deployment completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {str(e)}")
        return False

def main():
    """Main deployment function."""
    # Configuration for VM and deployment
    vm_details = {
        "subscription_id": "e6b341db-822e-4e47-8fef-a323f63c920d",
        "resource_group_name": "test-resource-group",
        "location": "East US",
        "vm_name": "test-windows-vm",
        "admin_username": "azureuser",
        "admin_password": "Password123!"  # In production, use secure password management
    }

    # Source directory containing your application
    source_directory = "./workspace"

    # Execute deployment
    if deploy_to_vm(source_directory, vm_details):
        print("Application deployed successfully!")
    else:
        print("Deployment failed!")

if __name__ == "__main__":
    main()
