import os
import subprocess
from datetime import datetime, timedelta

REPO_FOLDER = "github-green-generator"
DAYS_TO_COVER = 365
COMMITS_PER_DAY = 4

def main():
    if not os.path.exists(REPO_FOLDER):
        os.makedirs(REPO_FOLDER)
    os.chdir(REPO_FOLDER)
    
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    log_file = "activity.txt"
    start_date = datetime.now() - timedelta(days=DAYS_TO_COVER)

    print(f"Generating backdated commits for the past {DAYS_TO_COVER} days...")

    for day in range(DAYS_TO_COVER + 1):
        current_date = start_date + timedelta(days=day)
        for commit_num in range(COMMITS_PER_DAY):
            timestamp = current_date.replace(hour=9 + (commit_num * 3), minute=10 * commit_num).strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_file, "a") as f:
                f.write(f"Commit on {timestamp}\n")
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = timestamp
            env["GIT_COMMITTER_DATE"] = timestamp
            
            subprocess.run(["git", "add", log_file], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Activity {timestamp}"],
                env=env,
                check=True,
                stdout=subprocess.DEVNULL
            )

    print("All backdated commits generated successfully!")

if __name__ == "__main__":
    main()