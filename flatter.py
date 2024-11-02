import re
import sys

contents: dict[str, set[str]] = {}
graph: dict[str, set[str]] = {}
indegree: dict[str, int] = {}

def construct_graph(path: str) -> None:
    if path in contents:
        return
    directory = path.split('/')[:-1]
    content = open(path).read()
    standard_headers = re.findall(r"#include *(\<.*\>)", content)
    headers = re.findall(r"#include *\"(.*)\"", content)
    raw = []
    for line in content.split('\n'):
        if not line.lstrip().startswith("#include") and not line.lstrip().startswith("#pragma once"):
            raw.append(line)
    contents[path] = '\n'.join(raw)
    indegree[path] = len(standard_headers) + len(headers)
    for header in standard_headers:
        graph.setdefault(header, set()).add(path)
    for header in headers:
        header = '/'.join(directory+[header])
        graph.setdefault(header, set()).add(path)
        construct_graph(header)

def compute_topology() -> list[str]:
    order = []
    for header in graph:
        if indegree.get(header, 0) == 0:
            order.append(header)
    for i in range(len(graph)):
        for header in graph[order[i]]:
            indegree[header] -= 1
            if indegree[header] == 0:
                order.append(header)
    return order

def main():
    target = sys.argv[1]
    output = sys.argv[2]
    construct_graph(target)
    order = compute_topology()
    file = open(output, "w")
    for header in order:
        if header.startswith("<") and header.endswith(">"):
            file.write("#include " + header + "\n")
        else:
            file.write(contents[header] + "\n")
    file.close()

main()
