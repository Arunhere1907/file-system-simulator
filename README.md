# 🌳 File System Simulator

A visual file system simulator built with **Python (FastAPI)** + **Vanilla JS** — no frontend build tools, no npm, just open and run.

> Core DSA logic written by me · Frontend, animations & API by Claude

---

## What it does

| Section | What you get |
|---|---|
| **Files** | Create / delete / rename / move files and folders |
| **Tree View** | Live SVG diagram of the entire file system |
| **Traversal** | Animated DFS (recursive & iterative) + BFS — watch the algorithm visit each node |
| **Search** | Animated search showing every node visited before finding a match |

---

## DSA concepts inside

| Concept | Where used |
|---|---|
| N-ary tree | The file system itself — each folder is a node with multiple children |
| DFS recursive | `dfs_recursive()` — uses Python's call stack |
| DFS iterative | `dfs_iterative()` — explicit stack, no recursion limit |
| BFS | `bfs()` — level-order using `collections.deque` |
| Tree serialisation | `to_dict()` converts the tree to JSON for the frontend |
| DFS/BFS with steps | `search_with_steps()` returns every visited node for animation |

---

## Project structure

```
fs-sim/
├── backend/
│   ├── filesystem.py     ← Core DSA logic (TreeNode + FileSystem class)
│   ├── main.py           ← FastAPI routes
│   └── requirements.txt
├── frontend/
│   └── index.html        ← Complete frontend (zero build tools needed)
└── README.md
```

---

## Running locally

### 1 — Backend

```bash
cd backend

# create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

API now running at **http://localhost:8000**
Docs at **http://localhost:8000/docs**

### 2 — Frontend

No npm, no build step. Just open the file:

```bash
# Mac
open frontend/index.html

# Windows
start frontend/index.html

# Or drag frontend/index.html into any browser
```

> If you get CORS issues opening as a file, run a quick local server:
> ```bash
> cd frontend
> python -m http.server 3000
> # then open http://localhost:3000
> ```

---

## API reference

| Method | Route | Body | What it does |
|---|---|---|---|
| GET | `/tree` | — | Full file system as JSON |
| POST | `/create` | `{parent_path, name, node_type}` | Create file or folder |
| DELETE | `/delete` | `{path}` | Delete node + children |
| PUT | `/rename` | `{path, new_name}` | Rename node |
| PUT | `/move` | `{src_path, dest_path}` | Move node |
| POST | `/search` | `{name, method}` | DFS/BFS search with step trace |
| GET | `/traversal/{method}` | — | Full traversal order |

---

## Push to GitHub

```bash
# from the fs-sim/ root folder

git init
git add .
git commit -m "feat: file system simulator with DFS/BFS animations"

# create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/fs-sim.git
git branch -M main
git push -u origin main
```

---

## Credits

- **Core DSA logic** — written by me (TreeNode class, FileSystem operations, DFS/BFS traversals)
- **FastAPI routes, frontend UI, animations** — built with [Claude](https://claude.ai)
- Stack: Python · FastAPI · Vanilla JS · SVG animations
