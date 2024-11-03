import os
import re
import sys

contents: dict[str, list[str]] = {}
graph: dict[str, list[str]] = {}
indegree: dict[str, int] = {}

def get_content(path: str) -> str:
    try:
        with open(path) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        exit(0)

def construct_graph(path: str) -> None:
    if path in contents:
        return

    content = get_content(path)

    directory = os.path.dirname(path)

    standard_headers = re.findall(r"#include *(\<[^>]+\>)", content)
    headers = re.findall(r"#include *\"([^\"]+)\"", content)

    indegree[path] = len(standard_headers) + len(headers)

    raw = [
        line for line in content.splitlines()
        if not line.lstrip().startswith("#include") and not line.lstrip().startswith("#pragma once")
    ]
    contents[path] = '\n'.join(raw)

    for header in standard_headers:
        graph.setdefault(header, set()).append(path)

    for header in headers:
        header = os.path.abspath(os.path.join(directory, header))
        graph.setdefault(header, set()).append(path)
        construct_graph(header)

def compute_topology() -> list[str]:
    order = [header for header in graph if indegree.get(header, 0) == 0]

    for i in range(len(graph)):

        if i >= len(graph):
            print("Error: cycle detected in the dependency graph.")
            exit(0)

        for header in graph[order[i]]:
            indegree[header] -= 1
            if indegree[header] == 0:
                order.append(header)

    return order

def main():
    if len(sys.argv) < 3:
        print("Usage: python flatter.py <target_file> <output_file>")
        return

    target = sys.argv[1]
    output = sys.argv[2]

    construct_graph(target)
    order = compute_topology()

    with open(output, "w") as file:
        for header in order:
            if header.startswith("<") and header.endswith(">"):
                file.write(f"#include {header}\n")
            else:
                file.write(contents[header]+"\n")

main()
