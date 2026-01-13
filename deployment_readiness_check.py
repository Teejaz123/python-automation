import os
import socket
import subprocess
import sys

# ---- CONFIG ----

REQUIRED_ENV_VARS = [
    "APP_ENV",
    "DATABASE_URL",
    "AWS_REGION"
]

DEPENDENCIES = [
    ("Database", "localhost", 5432),  # Example: Postgres
]

ALLOWED_BRANCHES = ["main", "master"]

TIMEOUT = 3


# ---- CHECKS ----

def check_env_vars():
    missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    return True


def check_dependencies():
    for name, host, port in DEPENDENCIES:
        try:
            socket.create_connection((host, port), timeout=TIMEOUT)
            print(f"✅ {name} reachable")
        except Exception:
            print(f"❌ {name} unreachable ({host}:{port})")
            return False
    return True


def check_git_branch():
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        print("❌ Not a git repository")
        return False

    if branch not in ALLOWED_BRANCHES:
        print(f"❌ Deployments not allowed from branch '{branch}'")
        return False

    print(f"✅ Branch '{branch}' approved for deployment")
    return True


# ---- MAIN ----

def main():
    checks = [
        check_env_vars(),
        check_dependencies(),
        check_git_branch()
    ]

    if not all(checks):
        print("\n🚫 Deployment readiness check FAILED")
        sys.exit(1)

    print("\n🚀 Deployment readiness check PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()

