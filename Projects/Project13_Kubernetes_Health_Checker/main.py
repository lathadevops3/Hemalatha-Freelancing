import argparse
import subprocess


def kubectl_available():
    try:
        subprocess.run(["kubectl", "version", "--client"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def get_pods():
    if not kubectl_available():
        print("kubectl not available on this system.")
        return
    subprocess.run(["kubectl", "get", "pods", "--all-namespaces"])


def get_nodes():
    if not kubectl_available():
        print("kubectl not available on this system.")
        return
    subprocess.run(["kubectl", "get", "nodes"])


def demo():
    print("Kubernetes Health Checker Demo")
    get_nodes()
    get_pods()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        print("Run with --demo to inspect nodes and pods (requires kubectl).")


if __name__ == "__main__":
    main()
