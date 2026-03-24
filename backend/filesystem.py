from collections import deque


class TreeNode:
    def __init__(self, name, node_type):
        self.name = name          # file or folder name
        self.node_type = node_type  # "file" or "folder"
        self.children = []        # list of TreeNode  (folders only, but we store for files too)
        self.parent = None        # parent TreeNode reference


class FileSystem:
    def __init__(self):
        self.root = TreeNode("/", "folder")
        self._seed()

    def _seed(self):
        """Pre-populate with some demo data so the UI isn't empty."""
        self.create("/", "home", "folder")
        self.create("/home", "user", "folder")
        self.create("/home/user", "documents", "folder")
        self.create("/home/user", "pictures", "folder")
        self.create("/home/user", "music", "folder")
        self.create("/home/user/documents", "resume.pdf", "file")
        self.create("/home/user/documents", "notes.txt", "file")
        self.create("/home/user/documents", "project.py", "file")
        self.create("/home/user/pictures", "vacation.jpg", "file")
        self.create("/home/user/pictures", "profile.png", "file")
        self.create("/home/user/music", "playlist.mp3", "file")
        self.create("/", "etc", "folder")
        self.create("/etc", "config.yaml", "file")
        self.create("/etc", "hosts", "file")
        self.create("/", "var", "folder")
        self.create("/var", "logs", "folder")
        self.create("/var/logs", "app.log", "file")

    # ────────────────────────────────────────────────────────────────────────────
    # Path helpers
    # ────────────────────────────────────────────────────────────────────────────

    def get_node(self, path: str):
        """Walk the tree by path string like '/home/user/docs'."""
        if path in ("", "/"):
            return self.root
        parts = path.strip("/").split("/")
        curr = self.root
        for part in parts:
            found = next((c for c in curr.children if c.name == part), None)
            if not found:
                return None
            curr = found
        return curr

    def get_path(self, node) -> str:
        """Reconstruct full path string from a node reference."""
        if node is self.root:
            return "/"
        parts = []
        curr = node
        while curr is not self.root:
            parts.append(curr.name)
            curr = curr.parent
        return "/" + "/".join(reversed(parts))

    # ────────────────────────────────────────────────────────────────────────────
    # Core file-system operations
    # ────────────────────────────────────────────────────────────────────────────

    def create(self, parent_path: str, name: str, node_type: str) -> dict:
        parent = self.get_node(parent_path)
        if parent is None:
            return {"ok": False, "error": f"Path '{parent_path}' not found"}
        if parent.node_type != "folder":
            return {"ok": False, "error": f"'{parent_path}' is not a folder"}
        if any(c.name == name for c in parent.children):
            return {"ok": False, "error": f"'{name}' already exists"}
        node = TreeNode(name, node_type)
        node.parent = parent
        parent.children.append(node)
        return {"ok": True, "path": self.get_path(node)}

    def delete(self, path: str) -> dict:
        node = self.get_node(path)
        if node is None:
            return {"ok": False, "error": "Path not found"}
        if node is self.root:
            return {"ok": False, "error": "Cannot delete root"}
        node.parent.children.remove(node)
        node.parent = None
        return {"ok": True}

    def rename(self, path: str, new_name: str) -> dict:
        node = self.get_node(path)
        if node is None:
            return {"ok": False, "error": "Path not found"}
        if node is self.root:
            return {"ok": False, "error": "Cannot rename root"}
        if node.parent and any(s.name == new_name for s in node.parent.children if s is not node):
            return {"ok": False, "error": f"'{new_name}' already exists here"}
        node.name = new_name
        return {"ok": True, "new_path": self.get_path(node)}

    def move(self, src_path: str, dest_path: str) -> dict:
        node = self.get_node(src_path)
        dest = self.get_node(dest_path)
        if node is None:
            return {"ok": False, "error": f"Source '{src_path}' not found"}
        if dest is None:
            return {"ok": False, "error": f"Destination '{dest_path}' not found"}
        if dest.node_type != "folder":
            return {"ok": False, "error": "Destination must be a folder"}
        if node is self.root:
            return {"ok": False, "error": "Cannot move root"}
        # Guard: prevent moving a folder into its own subtree
        cur = dest
        while cur is not None:
            if cur is node:
                return {"ok": False, "error": "Cannot move folder into itself"}
            cur = cur.parent
        node.parent.children.remove(node)
        node.parent = dest
        dest.children.append(node)
        return {"ok": True, "new_path": self.get_path(node)}

    # ────────────────────────────────────────────────────────────────────────────
    # Traversals (your code, fixed to live inside the class)
    # ────────────────────────────────────────────────────────────────────────────

    def dfs_recursive(self, node=None) -> list:
        """Pre-order DFS using the call stack (recursion)."""
        if node is None:
            node = self.root
        result = []

        def dfs(curr):
            result.append(self.get_path(curr))
            for child in curr.children:
                dfs(child)

        dfs(node)
        return result

    def dfs_iterative(self, node=None) -> list:
        """Pre-order DFS using an explicit stack — no recursion limit."""
        if node is None:
            node = self.root
        stack = [node]
        result = []
        while stack:
            curr = stack.pop()
            result.append(self.get_path(curr))
            for child in reversed(curr.children):  # reversed keeps left-to-right order
                stack.append(child)
        return result

    def bfs(self, node=None) -> list:
        """Level-order BFS using a queue."""
        if node is None:
            node = self.root
        queue = deque([node])
        result = []
        while queue:
            curr = queue.popleft()
            result.append(self.get_path(curr))
            for child in curr.children:
                queue.append(child)
        return result

    def search(self, name: str) -> list:
        """DFS search — returns list of full paths matching name (case-insensitive)."""
        results = []

        def dfs(node):
            if node.name.lower() == name.lower():
                results.append(self.get_path(node))
            for child in node.children:
                dfs(child)

        dfs(self.root)
        return results

    def search_with_steps(self, name: str, method: str = "dfs") -> dict:
        """
        Returns every node visited in order (for animation) + matches.
        method: 'dfs' | 'bfs'
        """
        visited = []
        matches = []

        if method == "bfs":
            queue = deque([self.root])
            while queue:
                curr = queue.popleft()
                path = self.get_path(curr)
                visited.append(path)
                if curr.name.lower() == name.lower():
                    matches.append(path)
                for child in curr.children:
                    queue.append(child)
        else:
            def dfs(node):
                path = self.get_path(node)
                visited.append(path)
                if node.name.lower() == name.lower():
                    matches.append(path)
                for child in node.children:
                    dfs(child)
            dfs(self.root)

        return {"visited": visited, "matches": matches}

    # ────────────────────────────────────────────────────────────────────────────
    # Serialisation
    # ────────────────────────────────────────────────────────────────────────────

    def to_dict(self, node=None) -> dict:
        """Recursively turn the tree into a JSON-serialisable dict."""
        if node is None:
            node = self.root
        result = {
            "name": node.name,
            "type": node.node_type,
            "path": self.get_path(node),
        }
        if node.node_type == "folder":
            result["children"] = [self.to_dict(c) for c in node.children]
        else:
            result["children"] = []
        return result
