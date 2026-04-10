# Event Bus

## Role

The Event Bus decouples every stage of the pipeline. Producers publish events; consumers subscribe and process them independently. Neither side knows about the other.

## Interface

```cpp
class EventBus {
public:
    /// Push an event onto the queue (called by the Collector / Enrichment).
    void publish(const Event& e);

    /// Register a handler invoked for every published event.
    void subscribe(std::function<void(const Event&)> handler);
};
```

## Implementation

```
┌────────────┐   publish()    ┌─────────────────────────┐
│ Collector  │ ─────────────▶ │  std::queue<Event>       │
└────────────┘                │  (mutex + condvar)       │
                               └──────────┬──────────────┘
                                          │ notify
                          ┌───────────────┼──────────────────┐
                          ▼               ▼                  ▼
                    [Enrichment]    [Rule Engine]      [Metrics]
                    (consumer 1)    (consumer 2)      (consumer N)
```

- **Thread model:** 1 producer thread (Collector), N consumer threads (one per subscriber).
- **Synchronisation:** `std::queue<Event>` protected by `std::mutex` + `std::condition_variable`.
- **Backpressure (Phase 2):** bounded queue with configurable max capacity; producer blocks when full.

## Usage

```cpp
EventBus bus;

// Subscribe enrichment stage
bus.subscribe([&enricher](const Event& e) {
    enricher.process(e);
});

// Collector publishes
bus.publish(event);
```
