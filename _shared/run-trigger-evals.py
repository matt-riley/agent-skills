#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import signal
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run_copilot(prompt, model, timeout_seconds):
    cmd = ['copilot', '-p', prompt, '--output-format', 'json', '--allow-all-tools', '--no-ask-user', '--stream', 'off', '--model', model]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
        lines = [json.loads(line) for line in stdout.splitlines() if line.strip()]
        return proc.returncode, lines, stderr, False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        lines = [json.loads(line) for line in stdout.splitlines() if line.strip()]
        return 124, lines, stderr, True


def main():
    ap = argparse.ArgumentParser(description='Run trigger eval queries and detect whether a specific skill was selected.')
    ap.add_argument('trigger_queries')
    ap.add_argument('--skill-name')
    ap.add_argument('--runs', type=int, default=1)
    ap.add_argument('--max-queries', type=int)
    ap.add_argument('--model', default='gpt-5.4')
    ap.add_argument('--timeout', type=int, default=120)
    ap.add_argument('--static', action='store_true', help='Validate and summarize fixtures without invoking a specific agent harness.')
    default_output_root = Path(__file__).resolve().parent / 'results' / 'triggers'
    ap.add_argument('--output-root', default=str(default_output_root))
    args = ap.parse_args()
    trigger_path = Path(args.trigger_queries)
    skill_name = args.skill_name or trigger_path.parent.parent.name
    queries = json.loads(trigger_path.read_text())
    if args.max_queries:
        queries = queries[:args.max_queries]
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    out_dir = Path(args.output_root) / skill_name / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.static:
        positives = sum(1 for item in queries if item.get('should_trigger') is True)
        negatives = sum(1 for item in queries if item.get('should_trigger') is False)
        summary = {'skill_name': skill_name, 'mode': 'static', 'generated_at': timestamp, 'queries': len(queries), 'positives': positives, 'negatives': negatives, 'results': queries}
        (out_dir / 'results.json').write_text(json.dumps(summary, indent=2))
        print(json.dumps({'status': 'ok', 'mode': 'static', 'output_dir': str(out_dir), 'queries': len(queries), 'positives': positives, 'negatives': negatives}))
        return 0
    results = []
    for item in queries:
        runs = []
        for run in range(args.runs):
            code, lines, stderr, timed_out = run_copilot(item['query'], args.model, args.timeout)
            tool_requests = []
            final_message = ''
            session_usage = None
            for line in lines:
                if line.get('type') == 'assistant.message':
                    tool_requests.extend(line['data'].get('toolRequests') or [])
                    final_message = line['data'].get('content', final_message)
                elif line.get('type') == 'result':
                    session_usage = line.get('usage')
            used_skill = any(req.get('name') == 'skill' and req.get('arguments', {}).get('skill') == skill_name for req in tool_requests)
            runs.append({'run_index': run, 'exit_code': code, 'timed_out': timed_out, 'used_skill': used_skill, 'tool_requests': tool_requests, 'final_message': final_message, 'usage': session_usage, 'stderr': stderr})
        trigger_count = sum(1 for run in runs if run['used_skill'])
        results.append({'query': item['query'], 'should_trigger': item['should_trigger'], 'triggers': trigger_count, 'runs': args.runs, 'trigger_rate': trigger_count / args.runs, 'details': runs})
    summary = {'skill_name': skill_name, 'model': args.model, 'generated_at': timestamp, 'results': results}
    (out_dir / 'results.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({'status': 'ok', 'output_dir': str(out_dir), 'queries': len(results)}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
