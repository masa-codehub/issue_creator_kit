import subprocess


class GitAdapter:
    def run_command(self, command: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git"] + command, check=True, capture_output=True, text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e.stderr}") from e

    def checkout(self, branch: str, create: bool = False):
        cmd = ["checkout"]
        if create:
            cmd.append("-b")
        cmd.append(branch)
        self.run_command(cmd)

    def add(self, paths: list[str]):
        self.run_command(["add"] + paths)

    def commit(self, message: str):
        self.run_command(["commit", "-m", message])

    def push(
        self, remote: str = "origin", branch: str = "main", set_upstream: bool = False
    ):
        cmd = ["push"]
        if set_upstream:
            cmd.extend(["-u", remote, branch])
        else:
            cmd.extend([remote, branch])
        self.run_command(cmd)
