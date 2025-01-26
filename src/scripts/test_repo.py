from repository_manager import RepositoryManager
import os
import shutil
from repository_analysis import analyze_repository

def test_repository_manager():
    # Initialize the repository manager
    repo_manager = RepositoryManager()
    
    # Test cases
    test_cases = [
        # Test GitHub repository
        {
            "name": "GitHub Test",
            "source": "https://github.com/Arvo-AI/hello_world",  # Using Flask as an example
        },
        # Test local zip file (assuming you have a test.zip in deployai folder)
        {
            "name": "Zip Test",
            "source": "test.zip"  # Make sure this file exists in deployai/ folder
        }
    ]
    
    for test in test_cases:
        print(f"\n=== Running {test['name']} ===")
        try:
            # Process the repository
            repo_path = repo_manager.get_repository(test['source'])
            
            if repo_path:
                print(f"Success! Repository processed at: {repo_path}")
                print(f"Contents of directory:")
                for item in os.listdir(repo_path):
                    print(f"  - {item}")
                
                # Clean up
                repo_manager.cleanup(repo_path)
                print("Cleanup completed")
            else:
                print("Failed to process repository")
                
        except Exception as e:
            print(f"Error: {str(e)}")

def test_repository_analysis():
    """Test the repository analysis functionality"""
    # Setup
    repo_manager = RepositoryManager()
    test_cases = [
        {
            "name": "Flask Hello World",
            "source": "https://github.com/Arvo-AI/hello_world",
            "expected": {
                "hasDockerfile": False,
                "frameworks": ["Flask"],
                "exposedPorts": [5000],
            }
        }
        # Add more test cases as needed
    ]
    
    for test in test_cases:
        print(f"\nTesting analysis for: {test['name']}")
        try:
            # Get repository
            repo_path = repo_manager.get_repository(test["source"])
            if not repo_path:
                print(f"Failed to process repository for {test['name']}")
                continue
                
            # Analyze repository
            analysis = analyze_repository(repo_path)
            print(f"Analysis results: {analysis}")
            
            # Verify expected results
            for key, expected_value in test["expected"].items():
                actual_value = analysis[key]
                if key in ["frameworks", "exposedPorts"]:
                    # For lists, check if all expected items are present
                    all_present = all(item in actual_value for item in expected_value)
                    assert all_present, f"Expected {expected_value} to be in {actual_value}"
                else:
                    assert actual_value == expected_value, f"Expected {expected_value} but got {actual_value}"
                print(f"✓ Verified {key}: {actual_value}")
            
        except Exception as e:
            print(f"Error testing {test['name']}: {str(e)}")
            raise e
        finally:
            # Cleanup
            if repo_path and os.path.exists(repo_path):
                shutil.rmtree(repo_path)

if __name__ == "__main__":
    test_repository_manager()
    test_repository_analysis() 