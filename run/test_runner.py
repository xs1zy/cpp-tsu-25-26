#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

GHA_ERROR = "::error::"

def run_cmd(cmd, stdin_path=None, stdout_path=None, stderr_path=None, timeout=None):
    stdin = open(stdin_path, 'rb') if stdin_path else None
    stdout = open(stdout_path, 'wb') if stdout_path else subprocess.PIPE
    stderr = open(stderr_path, 'wb') if stderr_path else subprocess.PIPE
    try:
        proc = subprocess.run(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            timeout=timeout,
            check=False,
        )
        rc = proc.returncode
        out = b"" if stdout_path else (proc.stdout or b"")
        err = b"" if stderr_path else (proc.stderr or b"")
        return rc, out, err
    finally:
        if stdin:
            stdin.close()
        if stdout_path:
            stdout.close()
        if stderr_path:
            stderr.close()


def main():
    p = argparse.ArgumentParser(description="Run solution against tests using cmp-file checker")
    p.add_argument("--solution", required=True, help="Path to solution binary")
    p.add_argument("--checker", required=True, help="Path to cmp-file checker binary")
    p.add_argument("--tests", required=True, help="Path to tests directory (with .t and .t.a files)")
    p.add_argument("--out", required=True, help="Output directory for logs and outputs")
    p.add_argument("--timeout", type=float, default=None, help="Optional per-test timeout in seconds")
    args = p.parse_args()

    sol = Path(args.solution)
    cmpf = Path(args.checker)
    tests_dir = Path(args.tests)
    out_dir = Path(args.out)

    if not sol.is_file():
        print(f"{GHA_ERROR}Solution binary not found at {sol}")
        return 2
    if not cmpf.is_file():
        print(f"{GHA_ERROR}Checker binary not found at {cmpf}")
        return 2
    if not tests_dir.is_dir():
        print(f"{GHA_ERROR}Tests directory not found at {tests_dir}")
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    tests = sorted(tests_dir.glob("*.t"))
    if not tests:
        print("No tests found; passing by default.")
        return 0

    for t in tests:
        name = t.name
        ans = t.with_suffix(t.suffix + ".a")  # 001.t -> 001.t.a
        if not ans.is_file():
            print(f"{GHA_ERROR}Missing answer file for {name} (expected {ans})")
            return 1

        out = out_dir / f"{name}.out"
        serr = out_dir / f"{name}.stderr"
        cmp_stderr = out_dir / f"{name}.cmp.stderr"

        # Run solution
        rc, _, _ = run_cmd([str(sol)], stdin_path=t, stdout_path=out, stderr_path=serr, timeout=args.timeout)
        if rc != 0:
            print(f"{GHA_ERROR}Runtime error on test {name}")
            try:
                err_txt = serr.read_text(errors='ignore')
                if err_txt.strip():
                    print(err_txt)
            except Exception:
                pass
            return rc if rc != 0 else 1

        # Run checker
        rc, _, err = run_cmd([str(cmpf), str(t), str(out), str(ans)], stderr_path=str(cmp_stderr))
        if rc != 0:
            print(f"{GHA_ERROR}Test {name} failed. Checker output:")
            try:
                cmp_msg = cmp_stderr.read_text(errors='ignore')
                if cmp_msg.strip():
                    print(cmp_msg)
            except Exception:
                pass
            return rc if rc != 0 else 1

        print(f"Passed: {name}")

    print("All tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
