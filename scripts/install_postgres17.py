
#!/usr/bin/env python3
import subprocess
import sys

def run(cmd, check=True):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result

def main():
    print("==> Installing dependencies...")
    run("apt install -y curl ca-certificates")

    print("\n==> Setting up PostgreSQL signing key...")
    run("install -d /usr/share/postgresql-common/pgdg")
    run(
        "curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail "
        "https://www.postgresql.org/media/keys/ACCC4CF8.asc"
    )

    print("\n==> Detecting Ubuntu codename...")
    codename = subprocess.check_output("lsb_release -cs", shell=True).decode().strip()
    print(f"    Detected: {codename}")

    print("\n==> Adding PGDG apt repository...")
    repo_line = (
        f"deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] "
        f"https://apt.postgresql.org/pub/repos/apt {codename}-pgdg main"
    )
    with open("/etc/apt/sources.list.d/pgdg.list", "w") as f:
        f.write(repo_line + "\n")
    print(f"    Written: {repo_line}")

    print("\n==> Updating apt package lists...")
    run("apt update")

    print("\n==> Installing PostgreSQL 17...")
    run("apt install -y postgresql-17")

    print("\n✅ PostgreSQL 17 installed successfully.")

if __name__ == "__main__":
    if subprocess.run("id -u", shell=True, capture_output=True).stdout.strip() != b"0":
        print("This script must be run as root. Try: sudo python3 install_postgres17.py")
        sys.exit(1)
    main()