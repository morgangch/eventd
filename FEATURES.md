# eventd Features

## Overview

`eventd` is an event-driven automation engine for system processes, combining:

- real-time event processing (`stdout`, `stderr`, `exec`, `fork`, `exit`)
- declarative automation through a YAML rule DSL
- automated actions (local CI/CD-like workflows)
- real-time observability and supervision

Legend:

- `[PLANNED]` defined but not implemented yet

## Core Engine

### Event Capture

- [PLANNED] capture `exec`, `fork`, `exit`, `stdout`, `stderr`
- [PLANNED] low-level eBPF integration for high-performance capture
- [PLANNED] fallback collectors via `/proc` and pipes
- [PLANNED] journald integration

### Event Enrichment

- [PLANNED] add PID/PPID, process name, executable path, UID/GID
- [PLANNED] add args (`argv`), working directory, optional environment
- [PLANNED] add cgroup and container metadata
- [PLANNED] reconstruct process ancestry tree

### Event Pipeline

- [PLANNED] internal async event bus
- [PLANNED] fully non-blocking processing
- [PLANNED] high-throughput stream processing

## Rule Engine (YAML DSL)

### Rule Structure

- [PLANNED] `on`: event triggers
- [PLANNED] `from`: source scope
- [PLANNED] `if`: conditional logic
- [PLANNED] `match`: content matching
- [PLANNED] `ignore`: filtering
- [PLANNED] `then`: actions

### Triggers (`on`)

- [PLANNED] `exec`, `fork`, `exit`, `stdout`, `stderr`
- [PLANNED] multi-event correlation

### Advanced Matching

- [PLANNED] regex
- [PLANNED] glob
- [PLANNED] exact
- [PLANNED] contains
- [PLANNED] structured matching (JSON/log payloads)

### Conditions (`if`)

- [PLANNED] user-based conditions
- [PLANNED] parent process constraints
- [PLANNED] argument and executable path constraints
- [PLANNED] container/cgroup/environment constraints

### Filtering (`ignore`)

- [PLANNED] parent filtering by name/PID/path
- [PLANNED] multi-criteria filtering (`any`)
- [PLANNED] container/cgroup filtering
- [PLANNED] ancestry chain filtering

### Correlation

- [PLANNED] `within` time windows
- [PLANNED] event combinations
- [PLANNED] sequence detection

### Stateful Rules

- [PLANNED] internal state storage
- [PLANNED] persistent state variables
- [PLANNED] increment/decrement operators
- [PLANNED] state-based conditions

### Rate Limiting and Safety

- [PLANNED] trigger cooldown
- [PLANNED] rate limiting by time window
- [PLANNED] infinite loop protection

### Scoring / Risk Engine

- [PLANNED] per-event scoring
- [PLANNED] trigger threshold
- [PLANNED] SIEM-like risk logic

## Actions (`then`)

### System Actions

- [PLANNED] kill process
- [PLANNED] restart service
- [PLANNED] run script/command
- [PLANNED] process isolation

### Webhooks

- [PLANNED] HTTP actions (POST/GET/...)
- [PLANNED] dynamic templating
- [PLANNED] custom headers
- [PLANNED] automatic retries
- [PLANNED] timeout handling

### Notifications

- [PLANNED] Discord
- [PLANNED] Slack
- [PLANNED] generic webhook channels

### Plugins

- [PLANNED] extensible plugin system
- [PLANNED] custom actions
- [PLANNED] external integrations

## Secrets and Configuration

- [PLANNED] `.env` support
- [PLANNED] environment variable loading
- [PLANNED] `${VAR}` interpolation
- [PLANNED] secret namespaces
- [PLANNED] secret masking in logs/UI
- [PLANNED] future secret manager integration

## Observability and UI

### Dashboard

- [PLANNED] global system view
- [PLANNED] key metrics (`events/s`, `triggers`, latency)

### Event Stream

- [PLANNED] real-time stream view
- [PLANNED] trigger visualization

### Rule Manager

- [PLANNED] YAML rule editor
- [PLANNED] enable/disable rules
- [PLANNED] hot reload

### Logs and Audit

- [PLANNED] event history
- [PLANNED] action history
- [PLANNED] full traceability

### Explainability

- [PLANNED] why a rule matched
- [PLANNED] which conditions passed/failed

### System Views

- [PLANNED] process tree
- [PLANNED] container view
- [PLANNED] cgroup view

## Developer Experience

- [PLANNED] dry-run mode
- [PLANNED] rule simulation
- [PLANNED] verbose engine debug logs
- [PLANNED] event replay

## Deployment

### Local

- [PLANNED] systemd service
- [PLANNED] standalone binary

### Container

- [PLANNED] Docker image
- [PLANNED] volume-based configuration

### Orchestration

- [PLANNED] Kubernetes support
- [PLANNED] agent mode

### Remote Mode

- [PLANNED] inbound webhooks as external triggers
- [PLANNED] HTTP API

## Advanced Capabilities

- [PLANNED] behavioral anomaly detection
- [PLANNED] multi-process correlation
- [PLANNED] system timeline analysis
- [PLANNED] SIEM-like compatibility
- [PLANNED] automatic sandbox/isolation responses

## Architecture Targets

- [PLANNED] clear component separation: collector (eBPF/system), event bus, rule engine, action executor, API/UI

## Product Vision

Build a hybrid platform between:

- local CI/CD automation
- event-driven rule engine
- observability tooling
- behavioral detection system
