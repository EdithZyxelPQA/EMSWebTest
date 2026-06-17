import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / "environment_parameter.json"


def load_nodes():
    with ENV_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("EMS", {}).get("executeNode", ["NODE1"])
    if isinstance(nodes, str):
        return [nodes]
    return nodes


def run_pytest_for_node(node_name, test_target, reruns_count):
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_target,
        "-v",
        "-s",
        f"--cmdopt={node_name}",
    ]
    if reruns_count > 0:
        cmd.append(f"--reruns={reruns_count}")

    print(f"\n================ Run node: {node_name} ================")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    print(f"================ Done node: {node_name}, rc={result.returncode} ================\n")
    return node_name, result.returncode


def main():
    default_nodes = load_nodes()
    node_input = input(f"Nodes [{', '.join(default_nodes)}]: ").strip()
    nodes = [node.strip() for node in node_input.split(",") if node.strip()] if node_input else default_nodes

    test_input = input("Pytest target [tests]: ").strip()
    test_target = test_input if test_input else "tests"

    reruns_input = input("Reruns [0]: ").strip()
    try:
        reruns_count = int(reruns_input) if reruns_input else 0
    except ValueError:
        reruns_count = 0

    results = [run_pytest_for_node(node, test_target, reruns_count) for node in nodes]
    failed = [node for node, code in results if code != 0]
    if failed:
        print(f"Failed nodes: {', '.join(failed)}")
        sys.exit(1)

    print("All selected nodes passed.")


if __name__ == "__main__":
    main()

