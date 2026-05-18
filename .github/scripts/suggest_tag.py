import os
import subprocess
from openai import OpenAI

# 1. Get commits since last tag
try:
    latest_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
    commit_logs = subprocess.check_output(["git", "log", f"{latest_tag}..HEAD", "--oneline"]).decode().strip()
except Exception:
    # Fallback if no tags exist yet
    latest_tag = "v0.0.0"
    commit_logs = subprocess.check_output(["git", "log", "--oneline"]).decode().strip()

if not commit_logs:
    print("none")
    exit()

# 2. Call the cheap LLM
client = OpenAI(api_key=os.environ.get("LLM_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini", # Extremely cheap model
    messages=[
        {"role": "system", "content": "You are a SemVer versioning bot. Output ONLY the next version tag based on commits. No explanations."},
        {"role": "user", "content": f"Current tag: {latest_tag}\nNew commits:\n{commit_logs}\nWhat is the next tag?"}
    ],
    max_tokens=10,
    temperature=0
)

print(response.choices[0].message.content.strip())
