#!/usr/bin/env python3
"""
Generate docs/components/rule-engine.md dynamically from:
  - proto/rules.schema.json  (rule contract)
  - proto/events.schema.json (event contract — used in condition examples)

Run manually:   python scripts/gen_rule_engine_docs.py
Run in CI/CD:   called automatically by the GitHub Pages workflow before mkdocs build.
"""
from __future__ import annotations

import json
import pathlib
import textwrap
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).parent.parent
RULES_SCHEMA = ROOT / "proto" / "rules.schema.json"
EVENTS_SCHEMA = ROOT / "proto" / "events.schema.json"
OUTPUT = ROOT / "docs" / "components" / "rule-engine.md"


def _prop_table(properties: dict, required: list) -> str:
    lines = [
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]
    for name, spec in properties.items():
        typ = spec.get("type", "—")
        if isinstance(typ, list):
            typ = " \\| ".join(typ)
        req = "✅" if name in required else "—"
        desc = spec.get("description", "—")
        lines.append(f"| `{name}` | `{typ}` | {req} | {desc} |")
    return "\n".join(lines)


def _render_action_props(action_spec: dict) -> str:
    props = action_spec.get("properties", {})
    req = action_spec.get("required", [])
    return _prop_table(props, req)


def generate() -> str:
    rules_schema = json.loads(RULES_SCHEMA.read_text())
    events_schema = json.loads(EVENTS_SCHEMA.read_text())

    rules_props = rules_schema.get("properties", {})
    rules_required = rules_schema.get("required", [])

    events_props = events_schema.get("properties", {})
    events_required = events_schema.get("required", [])

    action_spec = rules_props.get("action", {})
    action_props = action_spec.get("properties", {})
    action_required = action_spec.get("required", [])

    # -------------------------------------------------------------------
    # Build known action types from schema enum if present, else defaults
    # -------------------------------------------------------------------
    action_type_spec = action_props.get("type", {})
    known_action_types: list[str] = action_type_spec.get(
        "enum", ["log", "webhook", "shell", "kill", "restart"]
    )

    action_type_rows = "\n".join(
        f"| `{t}` | {'**MVP**' if t in ('log', 'webhook', 'shell') else 'Phase 2'} |"
        for t in known_action_types
    )

    # -------------------------------------------------------------------
    # Build known event types from schema enum if present, else defaults
    # -------------------------------------------------------------------
    event_type_spec = events_props.get("type", {})
    known_event_types: list[str] = event_type_spec.get(
        "enum", ["exec", "stdout", "stderr", "exit", "net"]
    )
    event_type_list = "\n".join(f"- `{t}`" for t in known_event_types)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    doc = textwrap.dedent(f"""\
    # Rule Engine

    <!-- THIS FILE IS AUTO-GENERATED — do not edit manually.
         Source: scripts/gen_rule_engine_docs.py
         Schemas: proto/rules.schema.json, proto/events.schema.json
         Last generated: {now} -->

    !!! info "Auto-generated"
        This page is rebuilt automatically from the JSON Schema contracts in `proto/`
        every time the documentation is deployed.  To update the rule or event model,
        edit the schema files — this page will reflect the changes on the next build.

    ## Role

    The Rule Engine evaluates declarative YAML rules against every enriched event that
    flows through the pipeline.  When a rule's condition matches an event, the
    corresponding action is dispatched to the Action Executor.

    ```
    Enrichment ──▶ Rule Engine ──▶ Action Executor
                   (YAML rules)
    ```

    ---

    ## Rule schema (`proto/rules.schema.json`)

    Schema ID: `{rules_schema.get("$id", "eventd/rules.schema.json")}`  
    Title: **{rules_schema.get("title", "Rule")}**

    ### Rule fields

    {_prop_table(rules_props, rules_required)}

    ### Action object fields

    {_render_action_props(action_spec)}

    ---

    ## Event schema reference (`proto/events.schema.json`)

    Conditions are evaluated against enriched events whose fields are defined in
    `proto/events.schema.json`.

    Schema ID: `{events_schema.get("$id", "eventd/events.schema.json")}`

    ### Event fields

    {_prop_table(events_props, events_required)}

    ### Known event types

    {event_type_list}

    ---

    ## Rule DSL

    Rules are written in YAML and loaded from the directory pointed to by
    `EVENTD_RULES_DIR` (default: `rules/`).

    ### Minimal rule

    ```yaml
    name: my-rule
    condition: "event.type == 'exit'"
    action:
      type: log
    ```

    ### Full rule

    ```yaml
    name: detect-python-crash
    condition: "event.type == 'exit' and event.process_name == 'python' and event.exit_code != 0"
    action:
      type: webhook
      params:
        url: "https://hooks.example.com/eventd"
        method: POST
    ```

    ---

    ## Available action types

    | Type | Status |
    |------|--------|
    {action_type_rows}

    See [Action Executor](action-executor.md) for full documentation on each type.

    ---

    ## Internal C++ structure

    ```cpp
    struct Condition {{ std::string expression; }};
    struct Action    {{ std::string type; std::map<std::string, std::string> params; }};

    class Rule {{
    public:
        std::string name;
        Condition   condition;
        Action      action;

        bool matches(const EnrichedEvent& event) const;
    }};
    ```

    ### Parsing

    Rules are parsed with [`yaml-cpp`](https://github.com/jbeder/yaml-cpp) and
    validated against `proto/rules.schema.json` before being loaded into the engine.

    ### Evaluation loop

    ```cpp
    for (const auto& rule : loaded_rules) {{
        if (rule.matches(enriched_event)) {{
            executor.execute(rule.action, enriched_event);
        }}
    }}
    ```

    ### Design constraints

    - Strict separation between YAML parsing and runtime evaluation.
    - Parsing occurs at startup (or on hot-reload in Phase 2); evaluation occurs on every event.
    - Rules are immutable once loaded.

    ---

    ## Hot-reload (Phase 2)

    The engine will watch `EVENTD_RULES_DIR` with `inotify`.  When a file changes,
    the new rules are parsed and validated in a shadow copy; the live set is atomically
    swapped only if validation succeeds.

    ---

    ## Schema source files

    | File | Purpose |
    |------|---------|
    | [`proto/rules.schema.json`](https://github.com/morgangch/eventd/blob/main/proto/rules.schema.json) | Rule contract |
    | [`proto/events.schema.json`](https://github.com/morgangch/eventd/blob/main/proto/events.schema.json) | Event wire format |
    """)

    return doc


if __name__ == "__main__":
    content = generate()
    OUTPUT.write_text(content)
    print(f"Generated {OUTPUT}")
