import os
import git
from typing import Optional
import shutil
import zipfile
import re
import stat

class RepositoryManager:
    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace_dir = workspace_dir
        os.makedirs(workspace_dir, exist_ok=True)
    
    def is_github_url(self, path: str) -> bool:
        """Check if the path is a GitHub URL"""
        github_pattern = r'^https?://github\.com/[\w-]+/[\w.-]+(?:\.git)?$'
        return bool(re.match(github_pattern, path))
    
    def get_repository(self, path: str) -> Optional[str]:
        """
        Handles both GitHub URLs and local zip files
        Returns the path to the extracted/cloned repository
        """
        try:
            if self.is_github_url(path):
                return self._download_repository(path)
            elif path.endswith('.zip'):
                return self._extract_zip(path)
            else:
                raise ValueError("Path must be either a GitHub URL or a .zip file")
                
        except Exception as e:
            print(f"Failed to process repository: {str(e)}")
            return None
    
    def _download_repository(self, repo_url: str) -> str:
        """Downloads a GitHub repository"""
        # Extract application name from the repo URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        app_name = repo_name  
        local_path = os.path.join(self.workspace_dir, app_name)
        
        # Clean up existing directory if it exists
        self.cleanup(local_path)  # Use cleanup method instead of direct rmtree
        
        # Clone the repository
        print(f"Cloning repository from {repo_url} to {local_path}")
        git.Repo.clone_from(repo_url, local_path)
        
        return local_path
    
    def _extract_zip(self, zip_path: str) -> str:
        """Extracts a zip file"""
        # Get absolute path if zip_path is relative
        if not os.path.isabs(zip_path):
            zip_path = os.path.join('deployai', zip_path)
            
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found at {zip_path}")
            
        # Create a folder name from the zip file name with 'app_' prefix
        folder_name = f"app_{os.path.splitext(os.path.basename(zip_path))[0]}"
        extract_path = os.path.join(self.workspace_dir, folder_name)
        
        # Clean up existing directory if it exists
        self.cleanup(extract_path) 
        
        # Extract the zip file
        print(f"Extracting zip file from {zip_path} to {extract_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            
        return extract_path
    
    def cleanup(self, repo_path: str):
        """Cleans up the extracted/downloaded repository"""
        if os.path.exists(repo_path):
            # On Windows, make files writable before removal
            def on_rm_error(func, path, exc_info):
                # Make the file writable if read-only
                os.chmod(path, stat.S_IWRITE)
                # Try the removal again
                os.unlink(path)
            
            shutil.rmtree(repo_path, onerror=on_rm_error) 

if __name__ == "__main__":
    # Example usage
    manager = RepositoryManager()
    
    # Example GitHub URL
    github_url = "https://github.com/Arvo-AI/hello_world"
    print("Processing GitHub URL...")
    repo_path = manager.get_repository(github_url)
    if repo_path:
        print(f"Repository cloned to: {repo_path}")
    
    # Example zip file path
    zip_file_path = "example.zip"
    print("Processing zip file...")
    repo_path = manager.get_repository(zip_file_path)
    if repo_path:
        print(f"Repository extracted to: {repo_path}") 
