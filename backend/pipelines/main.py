from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)
class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.post("/pipelines/parse")
async def parse_pipeline(data: PipelineData):
    num_nodes = len(data.nodes)
    num_edges = len(data.edges)

    # Build adjacency list
    graph = {node.id: [] for node in data.nodes}
    for edge in data.edges:
        graph[edge.source].append(edge.target)

    # Check if the graph is a DAG
    is_dag = check_if_dag(graph)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag,
    }


def check_if_dag(graph: Dict[str, List[str]]) -> bool:
    visited = set()
    stack = set()

    def visit(node):
        if node in stack:
            return False  # Cycle detected
        if node in visited:
            return True

        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if not visit(neighbor):
                return False
        stack.remove(node)
        return True

    for node in graph:
        if not visit(node):
            return False
    return True

@app.get("/")
def health_check():
    return {"status": "OK"}

