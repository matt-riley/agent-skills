#!/usr/bin/env python3
"""Deterministic fixture checks for the skills catalog.

A fixture is a small repo in a known-broken state plus a `check.sh` that exits 0
only when the work is actually done. No model judges anything: the verdict is a
program's exit code.

    python _shared/run-fixture-evals.py --check-only
        Prove every fixture fails in its pristine state (fixtures must be broken).

    python _shared/run-fixture-evals.py --only tsc-error-triage
        Run the agent on one fixture, then check it.

    python _shared/run-fixture-evals.py --baseline
        Same, with the skill disabled, for a with/without comparison.

Results land in `_shared/results/fixtures/<timestamp>/summary.json`.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
RESULTS = Path(__file__).resolve().parent / "results" / "fixtures"
SKILLS = Path(__file__).resolve().parent.parent / "skills"
GORELESER = os.environ.get(
    "GORELESER", "go run github.com/goreleaser/goreleaser/v2@latest"
)


def fixtures() -> list[Path]:
    return sorted(
        p for p in FIXTURES.iterdir()
        if p.is_dir() and (p / "check.sh").is_file() and (p / "TASK.md").is_file()
    )


def run_check(fixture: Path, workspace: Path) -> tuple[bool, str]:
    """Run the pristine check script against a workspace."""
    env = {**os.environ, "GORELESER": GORELESER}
    proc = subprocess.run(
        ["bash", str(fixture / "check.sh"), str(workspace)],
        capture_output=True, text=True, timeout=900, env=env,
    )
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output.splitlines()[-1] if output else ""


def prepare_task(fixture: Path, workspace: Path) -> None:
    """Copy the fixture into a scratch workspace with a git repo it can diff."""
    shutil.copytree(fixture, workspace, dirs_exist_ok=True)
    for name in ("TASK.md", "check.sh"):
        (workspace / name).unlink(missing_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=workspace, check=False)
    subprocess.run(
        ["git", "-c", "user.email=fixture@example.com", "-c", "user.name=fixture",
         "add", "-A"], cwd=workspace, check=False, capture_output=True,
    )
    subprocess.run(
        ["git", "-c", "user.email=fixture@example.com", "-c", "user.name=fixture",
         "commit", "-qm", "fixture"], cwd=workspace, check=False, capture_output=True,
    )


def link_catalog(workspace: Path) -> None:
    """Expose the catalog as a repo-level skill source for this workspace.

    Copilot discovers repo skills under `.agents/skills`; a symlink keeps the
    comparison honest without touching the user-level skill directory.
    """
    target = workspace / ".agents" / "skills"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.symlink_to(SKILLS)


def run_agent(workspace: Path, prompt: str, skill: str, model: str,
              timeout: int, baseline: bool) -> dict:
    cmd = [
        "copilot", "-p", prompt,
        "--output-format", "json", "--allow-all-tools", "--no-ask-user",
        "--stream", "off", "--model", model,
    ]
    if baseline:
        cmd.append("--excluded-tools=skill")
    try:
        proc = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True,
                              timeout=timeout)
        tail = (proc.stdout or "")[-2000:]
        return {"exit_code": proc.returncode, "tail": tail}
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "tail": "timeout"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check-only", action="store_true",
                    help="verify fixtures are broken; run no agent")
    ap.add_argument("--only", action="append", default=[],
                    help="limit to a fixture name (repeatable)")
    ap.add_argument("--model", default="gpt-5.4")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--baseline", action="store_true",
                    help="run the agent with the skill disabled")
    ap.add_argument("--keep", action="store_true", help="keep scratch workspaces")
    ap.add_argument("--output-root", default=str(RESULTS))
    args = ap.parse_args()

    selected = [f for f in fixtures() if not args.only or f.name in args.only]
    if not selected:
        print("no fixtures selected")
        return 2

    if args.check_only:
        broken = 0
        for fixture in selected:
            ok, line = run_check(fixture, fixture)
            status = "BROKEN (expected)" if not ok else "ALREADY PASSING"
            broken += not ok
            print(f"  {fixture.name:<32} {status:<20} {line[:70]}")
        print(f"\n{broken}/{len(selected)} fixtures fail in their pristine state")
        return 0 if broken == len(selected) else 1

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.output_root) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {"generated_at": stamp, "mode": "baseline" if args.baseline else "skill",
               "model": args.model, "cases": []}

    for fixture in selected:
        task = (fixture / "TASK.md").read_text(encoding="utf-8").strip()
        prompt = f"Use the {fixture.name} skill for this task if relevant.\n\n{task}"
        workspace = Path(tempfile.mkdtemp(prefix=f"fixture-{fixture.name}-"))
        prepare_task(fixture, workspace)
        if not args.baseline:
            link_catalog(workspace)
        agent = run_agent(workspace, prompt, fixture.name, args.model,
                          args.timeout, args.baseline)
        passed, line = run_check(fixture, workspace)
        if not args.keep:
            shutil.rmtree(workspace, ignore_errors=True)
        print(f"  {fixture.name:<32} {'PASS' if passed else 'FAIL':<6} {line[:70]}")
        summary["cases"].append({
            "fixture": fixture.name, "passed": passed, "check_output": line,
            "agent_exit": agent["exit_code"], "agent_tail": agent["tail"][-400:],
            "workspace": str(workspace) if args.keep else "",
        })

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    rate = sum(c["passed"] for c in summary["cases"]) / len(summary["cases"])
    print(f"\npass rate: {rate:.2f} ({sum(c['passed'] for c in summary['cases'])}/{len(summary['cases'])})")
    print(f"summary: {out_dir / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
