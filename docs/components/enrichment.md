# Enrichment Layer

## Role

Transform raw, minimal events received from the bus into rich, actionable records by attaching real-time process context from `/proc`.

## Enriched event example

```json
{
  "id":           "550e8400-e29b-41d4-a716-446655440000",
  "type":         "stdout",
  "pid":          1234,
  "ppid":         1,
  "process_name": "python",
  "parent_name":  "systemd",
  "exe":          "/usr/bin/python3",
  "args":         ["server.py", "--port", "8080"],
  "cwd":          "/opt/app",
  "container":    "docker",
  "cgroup":       "/docker/abc123def456",
  "timestamp":    1712759673
}
```

## `/proc` data sources

| Field | Source |
|-------|--------|
| `process_name` | `/proc/<pid>/status` → `Name:` |
| `exe` | `readlink /proc/<pid>/exe` |
| `args` | `/proc/<pid>/cmdline` (null-delimited) |
| `cwd` | `readlink /proc/<pid>/cwd` |
| `ppid` | `/proc/<pid>/status` → `PPid:` |
| `cgroup` | `/proc/<pid>/cgroup` |

## LRU cache

Reading `/proc` on every event is expensive. The enricher maintains a per-PID LRU cache with a **500 ms TTL**. After that, metadata is refreshed (to catch `exec` chains where the PID is reused).

## Container detection

If `/proc/<pid>/cgroup` contains `docker/` or `/containerd/`, `container` is set to `"docker"` or `"containerd"` respectively.

## Interface

```cpp
class Enricher {
public:
    EnrichedEvent enrich(const Event& raw);
};
```

The enriched event is then forwarded to the Rule Engine.
