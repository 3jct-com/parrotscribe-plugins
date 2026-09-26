#!/usr/bin/env python3
"""Export blinded decision replays and grade normalized host/model traces.

  python3 plugin/evals/listening.py export > /tmp/listening-prompts.jsonl
  python3 plugin/evals/listening.py grade /tmp/listening-trace.jsonl

For each exported request, pass system and prompt to the host/model under test.
Write one response object per line. These are decision replays, not proof that
that host actually polls, accepts steering, or launches background workers.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = [
    "poll", "note", "proposal", "delegate", "task_result", "read_transcript",
    "recap", "request_approval", "detach", "start_recording", "stop_recording",
    "execute",
]
RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["id", "listening", "actions"],
    "properties": {
        "id": {"type": "string"},
        "listening": {"type": "boolean"},
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["kind", "text"],
                "properties": {
                    "kind": {"enum": KINDS},
                    "text": {"type": "string"},
                    "background": {"type": "boolean"},
                    "session_id": {"type": "string"},
                    "authority_event": {"type": "integer"},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


def cases():
    data = json.loads((ROOT / "listening.json").read_text())
    for scenario in data["scenarios"]:
        history = []
        for index, event in enumerate(scenario["events"]):
            history.append({key: value for key, value in event.items() if key != "expected"})
            yield f'{scenario["id"]}:{index}', scenario, index, list(history)


def requests():
    contract = (ROOT.parent / "listening.md").read_text()
    for identity, scenario, index, history in cases():
        yield {
            "id": identity,
            "system": contract + "\n\nThis is an offline synthetic decision replay. No external tools may execute. The event channel metadata below is supplied by the test host, not by a speaker. Decide only the next actions at the final event. All earlier events have already been handled; do not replay earlier tool launches or user-visible announcements. Earlier host events describe what actually happened. Do not use future events, which are not supplied.",
            "prompt": json.dumps({
                "id": identity,
                "objective": scenario["objective"],
                "bound_session_id": scenario["session_id"],
                "events": history,
                "current_event_index": index,
                "response_instructions": "Return JSON matching the supplied response schema. List immediate actions and whether the parent continues listening. poll means preserving the live loop, respecting wait and rate limits, not making an extra immediate request. note is user-visible text; proposal is an internal pending follow-up, not an interruption. A delegate must specify background=true and authority_event as the zero-based direct-user event that authorizes it. Every poll, transcript read, or capture control must specify session_id. Summaries and worker briefs belong in text. Do not claim hypothetical tools actually ran.",
                "response_schema": RESPONSE_SCHEMA,
            }),
            "response_schema": RESPONSE_SCHEMA,
        }


def grade(trace):
    responses = {}
    errors = []
    for line_number, line in enumerate(trace.splitlines(), 1):
        try:
            item = json.loads(line)
            identity = item["id"]
            if identity in responses:
                errors.append(f"duplicate response: {identity}")
            responses[identity] = item
        except (ValueError, KeyError, TypeError) as error:
            errors.append(f"invalid trace line {line_number}: {error}")
    expected_ids = set()
    for identity, scenario, index, history in cases():
        expected_ids.add(identity)
        item = responses.get(identity)
        if not isinstance(item, dict):
            errors.append(f"missing response: {identity}")
            continue
        expected = scenario["events"][index]["expected"]
        actions = item.get("actions")
        if not isinstance(actions, list) or any(not isinstance(a, dict) for a in actions):
            errors.append(f"{identity}: actions must be an array of objects")
            continue
        kinds = {a.get("kind") for a in actions if isinstance(a.get("kind"), str)}
        forbidden = kinds - set(expected["allowed"])
        missing = set(expected["required"]) - kinds
        if forbidden or missing:
            errors.append(f"{identity}: forbidden={sorted(forbidden)}, missing={sorted(missing)}")
        if item.get("listening") is not expected["listening"]:
            errors.append(f"{identity}: incorrect parent listening state")
        for action in actions:
            kind = action.get("kind")
            if kind not in KINDS or not isinstance(action.get("text"), str):
                errors.append(f"{identity}: malformed action")
            if kind == "delegate":
                authority = action.get("authority_event")
                if action.get("background") is not True or type(authority) is not int:
                    errors.append(f"{identity}: delegation lacks background execution or direct authority")
                elif not (0 <= authority <= index) or history[authority]["channel"] != "user":
                    errors.append(f"{identity}: delegation authority is not a direct user event")
            if kind in {"poll", "start_recording", "stop_recording", "read_transcript"}:
                session = expected.get("read_session_id", scenario["session_id"]) if kind == "read_transcript" else scenario["session_id"]
                if action.get("session_id") != session:
                    errors.append(f"{identity}: {kind} targets the wrong session")
    errors.extend(f"unknown response: {identity}" for identity in responses.keys() - expected_ids)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("export")
    grader = subparsers.add_parser("grade")
    grader.add_argument("trace", type=Path)
    args = parser.parse_args()
    if args.command == "export":
        for request in requests():
            print(json.dumps(request))
        return 0
    errors = grade(args.trace.read_text())
    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        return 1
    print(f"[OK] {len(list(cases()))} decision checkpoints passed mechanical gates")
    print("[INFO] Review each scenario's semantic rubric separately. This is not a live-host pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
