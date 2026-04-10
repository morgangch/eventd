# eventd Architecture

## Objective

Build a system event engine with this end-to-end flow:

OS -> Events -> Pipeline -> Rules -> Actions -> Output (logs/webhooks/UI)

## Global View

```text
+---------------------+
|   Event Collector   |  <- eBPF / /proc / pipes
+----------+----------+
           |
           v
+---------------------+
|     Event Bus       |  <- async queue
+----------+----------+
           |
           v
+---------------------+
|  Enrichment Layer   |  <- context enrichment
+----------+----------+
           |
           v
+---------------------+
|    Rule Engine      |  <- YAML DSL
+----------+----------+
           |
           v
+---------------------+
|   Action Executor   |
+----------+----------+
           |
           v
+---------------------+
| Output (logs/UI/API)|
+---------------------+
```

## Runtime Flow

Event -> Bus -> Enrichment -> Rule Engine -> Action -> Output

## 1. Event Collector

### Role

Capture system events in real time.

### Sources

- eBPF (recommended long term)
- /proc
- pipes (stdout, stderr)
- journald

### C++ Interface (target)

```cpp
struct Event {
    std::string type;   // exec, stdout, stderr...
    int pid;
    int ppid;
    std::string data;   // log line, args...
    std::chrono::system_clock::time_point ts;
};
```

### MVP Scope

Do not start with eBPF.

Start with:
- subprocess monitoring
- stdout/stderr capture

## 2. Event Bus

### Role

Decouple all pipeline components.

### Interface (target)

```cpp
class EventBus {
public:
    void publish(const Event& e);
    void subscribe(std::function<void(Event)> handler);
};
```

### Implementation

- thread-safe queue (`std::queue` + `std::mutex`)
- 1 producer thread / N consumer threads

## 3. Enrichment Layer

### Role

Transform raw events into rich, actionable events.

### Enriched Event Example

```json
{
  "pid": 1234,
  "ppid": 1,
  "process_name": "python",
  "parent_name": "systemd",
  "exe": "/usr/bin/python3",
  "args": ["server.py"],
  "container": "docker",
  "timestamp": 123456789
}
```

### Implementation

- read metadata from `/proc/<pid>/`
- keep a cache for performance

## 4. Rule Engine

### Role

Evaluate YAML rules at runtime.

### Internal Structure

```cpp
class Rule {
public:
    Trigger trigger;
    Condition condition;
    Action action;
};
```

### Parsing

- library: `yaml-cpp`

### Runtime Logic

```cpp
if (rule.matches(event)) {
    executor.execute(rule.action, event);
}
```

### Design Constraint

Strictly separate:
- YAML parsing
- runtime evaluation

## 5. Action Executor

### Role

Execute actions triggered by matching rules.

### Action Types

- shell command
- kill process
- restart service
- webhook

### Interface (target)

```cpp
class ActionExecutor {
public:
    void execute(const Action& action, const Event& event);
};
```

### Constraint

Actions must run asynchronously to avoid blocking the pipeline.

## 6. Output Layer

### Role

Expose execution and system state to operators.

### MVP

- console logs
- JSON file output

### Future

- REST API (Flask or C++)
- web dashboard

## Technical Choices

### Languages

- Core: C++
- UI/API: Python (Flask/FastAPI) or Node

### C++ Libraries

- YAML: `yaml-cpp`
- HTTP: `cpr` or `libcurl`
- JSON: `nlohmann/json`

## Delivery Strategy

### Phase 1 (MVP)

- collector via subprocess + stdout/stderr
- in-memory event bus
- basic enrichment (`/proc`)
- YAML rule parsing + simple condition matching
- async action execution
- console + JSON output

### Phase 2

- journald collector
- richer matching and correlation
- webhook retries and timeouts
- API + first dashboard views

### Phase 3

- eBPF collector
- behavior/risk scoring
- SIEM-like timeline and advanced analytics
