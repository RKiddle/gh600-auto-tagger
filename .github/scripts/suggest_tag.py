import subprocess
import sys

def get_git_history():
    """Fetches the latest tag and the commit messages since that tag."""
    try:
        # Attempt to find the most recent tag
        latest_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
        
        # Get the commit logs between the latest tag and now
        commits = subprocess.check_output(["git", "log", f"{latest_tag}..HEAD", "--oneline"]).decode().strip()
        
    except subprocess.CalledProcessError:
        # If the repository has zero tags, catch the error and fallback
        latest_tag = "v0.0.0"
        commits = subprocess.check_output(["git", "log", "--oneline"]).decode().strip()
        
    return latest_tag, commits

if __name__ == "__main__":
    current_tag, commit_logs = get_git_history()
    
    # For now, we will just print them to test that our observation tool works
    print(f"Current Tag: {current_tag}")
    print(f"New Commits:\n{commit_logs}")
