import subprocess


class GitAdapter:
    def run_command(self, command: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git"] + command, check=True, capture_output=True, text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            if stderr:
                first_line = stderr.splitlines()[0]
                max_len = 200
                if len(first_line) > max_len:
                    first_line = first_line[: max_len - 3] + "..."
                message = f"Git command failed: {first_line}"
            else:
                message = "Git command failed"
            raise RuntimeError(message) from e

    def checkout(self, branch: str, create: bool = False, base: str | None = None):
        cmd = ["checkout"]
        if create:
            cmd.append("-b")
        cmd.append(branch)
        if create and base:
            cmd.append(base)
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

    def move_file(self, src: str, dst: str):
        self.run_command(["mv", src, dst])

    def get_added_files(self, base_ref: str, head_ref: str, path: str) -> list[str]:
        """
        Get a list of newly added files in the specified path.

        Note: This uses --diff-filter=A and --no-renames, meaning files moved via
        'git mv' will be detected as Added only if Git does not identify them
        as renames (based on similarity threshold).
        """
        cmd = [
            "diff-tree",
            "-r",
            "--no-commit-id",
            "--name-only",
            "--diff-filter=A",
            "--no-renames",
            base_ref,
            head_ref,
            "--",
            path,
        ]
        output = self.run_command(cmd)
        if not output:
            return []
        return output.splitlines()
