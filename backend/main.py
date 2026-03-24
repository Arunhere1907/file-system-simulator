from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from filesystem import FileSystem

app = FastAPI(title="File System Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

fs = FileSystem()


# ── Request models ─────────────────────────────────────────────────────────────

class CreateBody(BaseModel):
    parent_path: str
    name: str
    node_type: str  # "file" | "folder"

class DeleteBody(BaseModel):
    path: str

class RenameBody(BaseModel):
    path: str
    new_name: str

class MoveBody(BaseModel):
    src_path: str
    dest_path: str

class SearchBody(BaseModel):
    name: str
    method: str = "dfs"  # "dfs" | "bfs"


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "File System Simulator API"}


@app.get("/tree")
def get_tree():
    return fs.to_dict()


@app.post("/create")
def create(body: CreateBody):
    res = fs.create(body.parent_path, body.name, body.node_type)
    if not res["ok"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return {"tree": fs.to_dict(), "created_path": res["path"]}


@app.delete("/delete")
def delete(body: DeleteBody):
    res = fs.delete(body.path)
    if not res["ok"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return {"tree": fs.to_dict()}


@app.put("/rename")
def rename(body: RenameBody):
    res = fs.rename(body.path, body.new_name)
    if not res["ok"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return {"tree": fs.to_dict(), "new_path": res["new_path"]}


@app.put("/move")
def move(body: MoveBody):
    res = fs.move(body.src_path, body.dest_path)
    if not res["ok"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return {"tree": fs.to_dict(), "new_path": res["new_path"]}


@app.post("/search")
def search(body: SearchBody):
    steps = fs.search_with_steps(body.name, body.method)
    return {
        "visited": steps["visited"],
        "matches": steps["matches"],
        "method": body.method,
        "tree": fs.to_dict(),
    }


@app.get("/traversal/{method}")
def traversal(method: str):
    allowed = {"dfs_recursive", "dfs_iterative", "bfs"}
    if method not in allowed:
        raise HTTPException(status_code=400, detail=f"Method must be one of {allowed}")
    if method == "dfs_recursive":
        order = fs.dfs_recursive()
    elif method == "dfs_iterative":
        order = fs.dfs_iterative()
    else:
        order = fs.bfs()
    return {"order": order, "tree": fs.to_dict()}
