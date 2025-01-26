import subprocess
import os
from typing import Dict, Tuple, Optional

def generate_terraform_config(details: Dict[str, str], output_path: str = "./terraform") -> None:
    """
    Generate a Terraform configuration file for provisioning a Windows VM in Azure.

    Args:
        details (dict): A dictionary containing configuration details such as:
            - subscription_id (str): Azure subscription ID
            - resource_group_name (str): The name of the resource group
            - location (str): Azure region/location
            - vm_name (str): Name of the Windows VM
            - admin_username (str): Administrator username for the VM
            - admin_password (str): Administrator password for the VM
        output_path (str): Path to save the generated Terraform configuration file.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Extract relevant data from `details` (provide default values if not present)
    subscription_id = details.get("subscription_id", "e6b341db-822e-4e47-8fef-a323f63c920d")
    resource_group_name = details.get("resource_group_name", "example-resource-group")
    location = details.get("location", "East US")
    vm_name = details.get("vm_name", "example-windows-vm")
    vm_username = details.get("admin_username", "azureuser")
    vm_password = details.get("admin_password", "Password123!")  # Use secure password

    # Write the Terraform file
    with open(os.path.join(output_path, "main.tf"), "w") as tf_file:
        tf_file.write(f"""\
#  Provider & Resource Group
provider "azurerm" {{
  features {{}}
  # Replace with your subscription
  subscription_id = "{subscription_id}"
}}

resource "azurerm_resource_group" "rg" {{
  name     = "{resource_group_name}"
  location = "{location}"
}}

#  Virtual Network & Subnet
resource "azurerm_virtual_network" "vnet" {{
  name                = "example-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}}

resource "azurerm_subnet" "subnet" {{
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}}

#  Public IP & Network Interface
resource "azurerm_public_ip" "public_ip" {{
  name                = "winvm-public-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Basic"
}}

resource "azurerm_network_interface" "nic" {{
  name                = "winvm-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {{
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }}
}}

#  Windows VM
resource "azurerm_windows_virtual_machine" "winvm" {{
  name                = "{vm_name}"
  computer_name       = "winvm-test"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  size                = "Standard_B1s"

  admin_username = "{vm_username}"
  admin_password = "{vm_password}"

  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  os_disk {{
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }}

  source_image_reference {{
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }}
}}

#  Output
output "vm_public_ip" {{
  description = "Public IP of Windows VM"
  value       = azurerm_public_ip.public_ip.ip_address
}}
""")

def run_terraform_command(command: list, working_dir: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Function to execute a Terraform command.

    Args:
        command (list): The Terraform command to execute, provided as a list. Example: ["terraform", "init"]
        working_dir (str): The directory where the Terraform command will be executed.

    Returns:
        tuple: (stdout, stderr) The output of the command execution.
    """
    try:
        result = subprocess.run(
            command,
            cwd=working_dir,  # Execute in the directory containing Terraform files
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True,  # Output as string (not bytes)
            check=True,  # Raise exception on command failure
        )
        print(f"Command succeeded: {' '.join(command)}")
        print(f"Output:\n{result.stdout}")
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        print(f"Error Output:\n{e.stderr}")
        return None, e.stderr

def deploy_with_terraform() -> None:
    """
    Function to deploy infrastructure using Terraform.
    """
    terraform_dir = "./terraform"  

    # 1. Initialize Terraform
    print("Initializing Terraform...")
    init_command = ["terraform", "init"]
    _, init_error = run_terraform_command(init_command, terraform_dir)
    if init_error:
        print("Terraform init failed.")
        return

    # 2. Generate Terraform plan
    print("Generating Terraform plan...")
    plan_command = ["terraform", "plan", "-out=plan.tfplan"]
    _, plan_error = run_terraform_command(plan_command, terraform_dir)
    if plan_error:
        print("Terraform plan failed.")
        return

    # 3. Apply Terraform configuration
    print("Applying Terraform configuration...")
    apply_command = ["terraform", "apply", "-auto-approve", "plan.tfplan"]
    _, apply_error = run_terraform_command(apply_command, terraform_dir)
    if apply_error:
        print("Terraform apply failed.")
        return

    print("Terraform deployment completed successfully!")

# Example usage
if __name__ == "__main__":
    # Sample configuration details for testing
    sample_details = {
        "subscription_id": "e6b341db-822e-4e47-8fef-a323f63c920d",
        "resource_group_name": "test-resource-group",
        "location": "East US",
        "vm_name": "test-windows-vm",
        "admin_username": "azureuser",
        "admin_password": "Password123!"
    }

    # Path where the Terraform configuration will be generated
    output_path = "./terraform"

    # Generate the Terraform configuration
    print("Generating Terraform configuration...")
    generate_terraform_config(sample_details, output_path)

    # Deploy the infrastructure using Terraform
    print("Deploying infrastructure with Terraform...")
    deploy_with_terraform()
    
