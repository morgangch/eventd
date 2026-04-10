# Action Executor

## Role

Execute the actions triggered by the Rule Engine, asynchronously, without ever blocking the pipeline.

## Action types

| Type | Description | Status |
|------|-------------|--------|
| `log` | Write a structured log entry | **MVP** |
| `webhook` | HTTP POST to an external URL | **MVP** |
| `shell` | Execute a shell command | **MVP** |
| `kill` | Send a POSIX signal to a process | Phase 2 |
| `restart` | Restart a systemd service via D-Bus | Phase 2 |

## Interface

```cpp
struct Action {
    std::string type;
    std::map<std::string, std::string> params;
};

class ActionExecutor {
public:
    void execute(const Action& action, const Event& event);
};
```

## Threading model

All actions run on a **dedicated thread pool** (default: 4 workers). This ensures that a slow webhook or shell command never stalls the event bus or rule evaluation.

```
Rule Engine ──▶ ActionExecutor::execute()
                        │
                        ▼
              ┌─────────────────────┐
              │   Thread pool (4)   │
              │  worker │ worker    │
              │  worker │ worker    │
              └─────────────────────┘
```

## Action examples

=== "log"

    ```yaml
    action:
      type: log
      params:
        level: warning
        message: "High CPU process detected: {event.process_name}"
    ```

=== "webhook"

    ```yaml
    action:
      type: webhook
      params:
        url: "https://hooks.example.com/eventd"
        method: POST
        # body is auto-populated with the serialised event
    ```

=== "shell"

    ```yaml
    action:
      type: shell
      params:
        command: "notify-send 'eventd' 'Process {event.process_name} ({event.pid}) triggered rule {rule.name}'"
    ```

## Webhook retries (Phase 2)

Exponential back-off with configurable max attempts. Failed deliveries are logged to the output layer.
