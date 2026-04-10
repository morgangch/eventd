# Event Collector

## Role

The collector is the entry point of the eventd pipeline. It captures system events in real time and publishes them onto the Event Bus.

## Event sources

| Source | Status | Notes |
|--------|--------|-------|
| Subprocess + stdout/stderr | **MVP** | spawn a child process, capture line by line |
| `/proc` polling | **MVP** | used by the enrichment stage |
| journald | Phase 2 | systemd journal integration |
| eBPF | Phase 3 | kernel-level, lowest overhead, CO-RE |

## C++ struct

```cpp
struct Event {
    std::string id;    // UUID v4
    std::string type;  // exec | stdout | stderr | exit | net | …
    int         pid;
    int         ppid;
    std::string data;  // log line, argv, syscall argument, …
    std::chrono::system_clock::time_point ts;
};
```

## MVP implementation

1. Spawn a child process with `popen` or `fork/exec`.
2. Attach a non-blocking read loop to its `stdout` and `stderr` file descriptors.
3. On each newline, construct an `Event` and call `bus.publish(event)`.
4. On process exit, emit an `exit` event carrying the exit code.

## Wiring

```cpp
Collector collector(subprocess_path, argv);
collector.on_event([&bus](const Event& e) {
    bus.publish(e);
});
collector.start();
```

## Contract

Events are serialised to JSON according to [`proto/events.schema.json`](https://github.com/morgangch/eventd/blob/main/proto/events.schema.json) when leaving the core over the API.
