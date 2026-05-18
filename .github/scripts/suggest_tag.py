import subprocess
import sys
import os
import json
from google import genai
from google.genai import types

def get_git_history():
    """Fetches the latest tag and the commit messages."""
    try:
        latest_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        commits = subprocess.check_output(["git", "log", f"{latest_tag}..HEAD", "--oneline"]).decode().strip()
    except subprocess.CalledProcessError:
        latest_tag = "v0.0.0"
        commits = subprocess.check_output(["git", "log", "--oneline"]).decode().strip()
        
    return latest_tag, commits

def analyze_commits_with_llm(current_tag, commits):
    """Passes commits to Gemini using the new SDK and demands structured JSON."""
    # The new SDK automatically picks up the GEMINI_API_KEY environment variable
    client = genai.Client()

    system_prompt = """
    You are an expert DevOps release agent. Analyze the provided git commits.
    Based on Semantic Versioning (SemVer), determine the next version tag.
    
    Rules:
    - Major (vX.0.0): Breaking changes.
    - Minor (v0.X.0): New features, backward compatible.
    - Patch (v0.0.X): Bug fixes.
    
    You MUST respond with a valid JSON object using this exact schema:
    {
      "highest_impact_change": "brief description of the most significant change",
      "semver_type": "patch | minor | major",
      "reasoning": "why this semver type was chosen based on the commit history",
      "recommended_tag": "vX.Y.Z"
    }
    """

    user_prompt = f"Current Tag: {current_tag}\n\nCommits:\n{commits}"
    
    # Using the new Generation API structure
    response = client.models.generate_content(
        model='gemini-2.5-flash', # <--- UPDATED TO CURRENT MODEL
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    return json.loads(response.text)

if __name__ == "__main__":
    # Ensure the API key is set before proceeding
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    current_tag, commit_logs = get_git_history()
    
    if not commit_logs:
        print("none")
        sys.exit(0)
        
    print("Agent is analyzing commits...", file=sys.stderr)
    
    try:
        plan = analyze_commits_with_llm(current_tag, commit_logs)
        print(json.dumps(plan, indent=2), file=sys.stderr)
        print(plan["recommended_tag"])
    except Exception as e:
        print(f"Agent failed: {e}", file=sys.stderr)
        print("none")
        sys.exit(1)