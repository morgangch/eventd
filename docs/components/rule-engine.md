    # Rule Engine

    <!-- THIS FILE IS AUTO-GENERATED — do not edit manually.
         Source: scripts/gen_rule_engine_docs.py
         Schemas: proto/rules.schema.json, proto/events.schema.json
         Last generated: 2026-04-10 15:53 UTC -->

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

    Schema ID: `eventd/rules.schema.json`  
    Title: **Rule**

    ### Rule fields

    | Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ | — |
| `condition` | `string` | ✅ | — |
| `action` | `object` | ✅ | — |

    ### Action object fields

    | Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `string` | ✅ | — |
| `params` | `object` | — | — |

    ---

    ## Event schema reference (`proto/events.schema.json`)

    Conditions are evaluated against enriched events whose fields are defined in
    `proto/events.schema.json`.

    Schema ID: `eventd/events.schema.json`

    ### Event fields

    | Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ | — |
| `type` | `string` | ✅ | — |
| `timestamp` | `string` | ✅ | — |
| `source` | `string` | ✅ | — |
| `payload` | `object` | — | — |

    ### Known event types

    - `exec`
- `stdout`
- `stderr`
- `exit`
- `net`

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
    | `log` | **MVP** |
| `webhook` | **MVP** |
| `shell` | **MVP** |
| `kill` | Phase 2 |
| `restart` | Phase 2 |

    See [Action Executor](action-executor.md) for full documentation on each type.

    ---

    ## Internal C++ structure

    ```cpp
    struct Condition { std::string expression; };
    struct Action    { std::string type; std::map<std::string, std::string> params; };

    class Rule {
    public:
        std::string name;
        Condition   condition;
        Action      action;

        bool matches(const EnrichedEvent& event) const;
    };
    ```

    ### Parsing

    Rules are parsed with [`yaml-cpp`](https://github.com/jbeder/yaml-cpp) and
    validated against `proto/rules.schema.json` before being loaded into the engine.

    ### Evaluation loop

    ```cpp
    for (const auto& rule : loaded_rules) {
        if (rule.matches(enriched_event)) {
            executor.execute(rule.action, enriched_event);
        }
    }
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
