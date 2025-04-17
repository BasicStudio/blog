import subprocess
import os
from getpass import getpass

def git_pull_push_commit(repo_path, commit_message):
    """
    Pulls, commits, and pushes changes to a Git repository.  Handles errors
    and provides user feedback.  Uses subprocess for Git commands.

    Args:
        repo_path (str): The path to the local Git repository.
        commit_message (str): The message for the Git commit.
    """
    # Check if the repository path exists
    if not os.path.exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist.")
        return

    # Change the current working directory to the repository path
    try:
        os.chdir(repo_path)
    except OSError as e:
        print(f"Error: Could not change directory to '{repo_path}'. {e}")
        return

    # 1. Pull changes
    print("Pulling changes from the remote repository...")
    try:
        # Use subprocess.run for better control and error handling
        pull_result = subprocess.run(['git', 'pull'],
                                    capture_output=True,  # Capture output for error messages
                                    text=True)          # Decode output as text

        if pull_result.returncode != 0:
            print(f"Error pulling changes: {pull_result.stderr}")
            print(f"  (Command: git pull)") # add the git command
            return
        else:
            print(pull_result.stdout) # print the output of pull

    except Exception as e:
        print(f"An error occurred while pulling: {e}")
        return

    # 2. Commit changes
    print("Committing changes...")
    try:
        # Use subprocess.run for the commit command
        commit_result = subprocess.run(['git', 'commit', '-m', commit_message],
                                      capture_output=True,
                                      text=True)

        if commit_result.returncode != 0:
            # Check for the special case of "nothing to commit"
            if "nothing to commit" in commit_result.stdout:
                print("No changes to commit.")
                # We still want to try to push in this case
            else:
                print(f"Error committing changes: {commit_result.stderr}")
                print(f"  (Command: git commit -m \"{commit_message}\")") # add the git command
                return
        else:
             print(commit_result.stdout)

    except Exception as e:
        print(f"An error occurred while committing: {e}")
        return

    # 3. Push changes
    print("Pushing changes to the remote repository...")
    try:
        # Use subprocess.run for the push command
        push_result = subprocess.run(['git', 'push'],
                                    capture_output=True,
                                    text=True)

        if push_result.returncode != 0:
            print(f"Error pushing changes: {push_result.stderr}")
            print(f"  (Command: git push)")
            return
        else:
            print(push_result.stdout)

    except Exception as e:
        print(f"An error occurred while pushing: {e}")
        return

    print("Successfully pulled, committed, and pushed changes.")

if __name__ == "__main__":
    # Get the repository path and commit message from the user
    repo_path = input("Enter the path to your Git repository: ")
    commit_message = input("Enter the commit message: ")

    # Call the function to perform the Git operations
    git_pull_push_commit(repo_path, commit_message)
