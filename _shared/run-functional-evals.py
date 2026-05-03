#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run_copilot(
    prompt: str, model: str, timeout_seconds: int, exclude_skill: bool = False
) -> dict:
    cmd = [
        "copilot",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--allow-all-tools",
        "--no-ask-user",
        "--stream",
        "off",
        "--model",
        model,
    ]
    if exclude_skill:
        cmd.append("--excluded-tools=skill")
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
        exit_code = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        exit_code = 124
        timed_out = True
    lines = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    tool_requests = []
    final_message = ""
    usage = None
    for line in lines:
        if line.get("type") == "assistant.message":
            tool_requests.extend(line["data"].get("toolRequests") or [])
            final_message = line["data"].get("content", final_message)
        elif line.get("type") == "result":
            usage = line.get("usage")
    return {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "final_message": final_message,
        "tool_requests": tool_requests,
        "usage": usage,
        "stderr": stderr,
    }


def judge_response(
    skill_name: str, case: dict, response: str, model: str, timeout_seconds: int
) -> dict:
    prompt = "\n".join(
        [
            "Judge this skill-eval output.",
            "Return strict JSON only.",
            'Use this schema: {"assertion_results":[{"assertion":"...","passed":true,"evidence":"..."}],"summary":{"passed":0,"failed":0,"total":0,"pass_rate":0}}',
            f"Skill: {skill_name}",
            f"Prompt: {case['prompt']}",
            f"Expected behavior: {case['expected_behavior']}",
            f"Assertions: {json.dumps(case['assertions'])}",
            f"Response: {response}",
        ]
    )
    raw = run_copilot(prompt, model, timeout_seconds, exclude_skill=True)
    text = raw["final_message"].strip()
    try:
        return json.loads(text)
    except Exception:
        return {
            "assertion_results": [],
            "summary": {
                "passed": 0,
                "failed": len(case["assertions"]),
                "total": len(case["assertions"]),
                "pass_rate": 0,
                "parse_error": text,
            },
        }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run functional evals with skill-on and skill-excluded baselines."
    )
    ap.add_argument("evals_json")
    ap.add_argument("--skill-name")
    ap.add_argument("--model", default="gpt-5.4")
    ap.add_argument("--judge-model", default="gpt-5-mini")
    default_output_root = Path(__file__).resolve().parent / "results" / "functional"
    ap.add_argument(
        "--output-root",
        default=str(default_output_root),
    )
    ap.add_argument("--max-evals", type=int)
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    eval_path = Path(args.evals_json)
    payload = json.loads(eval_path.read_text())
    skill_name = args.skill_name or payload["skill_name"]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.output_root) / skill_name / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    cases = payload["evals"][: args.max_evals] if args.max_evals else payload["evals"]
    summary = {"skill_name": skill_name, "generated_at": timestamp, "cases": []}

    for case in cases:
        case_dir = out_dir / case["id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        with_skill = run_copilot(
            f"Use the {skill_name} skill for this task if relevant.\n\n{case['prompt']}",
            args.model,
            args.timeout,
        )
        baseline = run_copilot(
            case["prompt"], args.model, args.timeout, exclude_skill=True
        )
        with_skill_grading = judge_response(
            skill_name,
            case,
            with_skill["final_message"],
            args.judge_model,
            args.timeout,
        )
        baseline_grading = judge_response(
            skill_name,
            case,
            baseline["final_message"],
            args.judge_model,
            args.timeout,
        )
        (case_dir / "with_skill.json").write_text(
            json.dumps(
                {"case": case, "run": with_skill, "grading": with_skill_grading}, indent=2
            )
        )
        (case_dir / "baseline.json").write_text(
            json.dumps(
                {"case": case, "run": baseline, "grading": baseline_grading}, indent=2
            )
        )
        summary["cases"].append(
            {
                "id": case["id"],
                "with_skill": with_skill_grading.get("summary", {}),
                "baseline": baseline_grading.get("summary", {}),
            }
        )

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({"status": "ok", "output_dir": str(out_dir), "cases": len(summary["cases"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
