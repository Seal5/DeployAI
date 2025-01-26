import os

def check_configurations(workspace_path: str = "./workspace") -> dict:
    """
    Scans the workspace directory to see if any Python or Node configs exist.
    Returns a dictionary with booleans for Python or NPM needs:
        {
            "has_requirements": bool,  # True if requirements.txt is found
            "has_package_json": bool   # True if package.json is found
        }
    """
    result = {
        "has_requirements": False,
        "has_package_json": False
    }

    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if file.lower() == "requirements.txt":
                result["has_requirements"] = True
            elif file.lower() == "package.json":
                result["has_package_json"] = True

            # If both are found, we can exit early if desired
            if result["has_requirements"] and result["has_package_json"]:
                return result

    return result

def generate_dependency_script(has_package_json: bool, has_requirements: bool) -> None:
    """
    Creates a PowerShell script that installs Node or Python if needed,
    then runs npm install or pip install to fetch app dependencies.
    Assumes a Windows Server environment.
    Saves the script to src/scripts/install_dependencies.ps1
    """
    lines = [
        "# PowerShell script to install Node/Python & dependencies if needed",
        "Write-Host 'Starting dependency installation...'"
    ]

    if has_package_json:
        lines.append("""
Write-Host 'Installing Node.js...'
# Example for Node 16 on Windows:
# Download Node installer
Invoke-WebRequest -Uri "https://nodejs.org/dist/v16.20.1/node-v16.20.1-x64.msi" -OutFile "node-installer.msi"
Start-Process msiexec.exe -Wait -ArgumentList '/i node-installer.msi /qn /norestart'
Write-Host 'Node.js installed.'

Write-Host 'Running npm install...'
npm install
Write-Host 'npm install completed.'
""".strip())

    if has_requirements:
        lines.append("""
Write-Host 'Installing Python 3.9...'
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -OutFile "python-installer.exe"
Start-Process .\\python-installer.exe -Wait -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1'
Write-Host 'Python installed.'

Write-Host 'Installing pip dependencies...'
pip install -r requirements.txt
Write-Host 'pip install completed.'
""".strip())

    lines.append("Write-Host 'Dependency installation script finished.'")

    # Add command to run the application
    lines.append("Write-Host 'Starting the application...'")
    lines.append("python app.py")  # Adjust this line if your application entry point is different

    script_content = "\n".join(lines)
    
    # Create scripts directory if it doesn't exist
    script_dir = os.path.join("src", "scripts")
    os.makedirs(script_dir, exist_ok=True)
    
    # Save script to file
    script_path = os.path.join(script_dir, "install_dependencies.ps1")
    with open(script_path, "w") as f:
        f.write(script_content)

# Example usage:
if __name__ == "__main__":
    workspace = "./workspace"
    config_check = check_configurations(workspace)
    print(config_check)
    # e.g. -> {'has_requirements': True, 'has_package_json': False}

    # Test generate_dependency_script with the current configuration
    print("Generating dependency script based on current configuration...")
    generate_dependency_script(
        has_package_json=config_check["has_package_json"],
        has_requirements=config_check["has_requirements"]
    )
    script_path = os.path.join("src", "scripts", "install_dependencies.ps1")
    with open(script_path, "r") as f:
        content = f.read()
        print("Generated script content:")
        print(content)
