import argparse
import subprocess
from pathlib import Path


def docker_available():
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def list_containers():
    if not docker_available():
        print("Docker not available on this system.")
        return
    subprocess.run(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}"])


def stop_container(name):
    if not docker_available():
        print("Docker not available on this system.")
        return
    subprocess.run(["docker", "stop", name])


def start_container(name):
    if not docker_available():
        print("Docker not available on this system.")
        return
    subprocess.run(["docker", "start", name])


def demo():
    print("Docker Container Manager Demo")
    list_containers()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        print("Run with --demo to see available docker operations.")


if __name__ == "__main__":
    main()
