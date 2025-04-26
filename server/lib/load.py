from dotenv import load_dotenv
import os

vars = ["ANTHROPIC_API_KEY"]

def preflight():
    """Check for missing environment variables."""
    load_dotenv()

    missing_env_vars: list[str] = []

    for var in vars:
        if os.getenv(var) is None:
            missing_env_vars.append(var)

    if len(missing_env_vars) > 0:
        print(f"Missing environment variables: {', '.join(missing_env_vars)}")
        exit(1)
