# Quick Start

This page walks you through a complete eventd setup in under five minutes.

---

## 1. Start the stack

```bash
docker compose -f deploy/docker/docker-compose.yml up --build
```

You should see:

```
core-1     | eventd-core starting: internal-monitor-engine
backend-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
mcp-1      | INFO:     Uvicorn running on http://0.0.0.0:8100
frontend-1 | nginx/1.27 ready
```

---

## 2. Check the API

```bash
curl http://localhost:8000/status
```

---

## 3. Use the CLI

```bash
pip install -e ./cli
eventctl --help
```

---

## 4. Write your first rule

Create `rules/my-rules.yml`:

```yaml
name: detect-python-crash
condition: "event.type == 'exit' and event.process_name == 'python' and event.exit_code != 0"
action:
  type: log
  params:
    level: warning
    message: "Python process crashed (pid={event.pid})"
```

!!! note
    Rule hot-loading is planned for Phase 2. For now, restart the core to pick up new rules.

---

## 5. Explore the dashboard

Open [http://localhost:3000](http://localhost:3000) in your browser to see the live event feed.

---

## Next steps

- Read the [Architecture](../architecture.md) to understand the full pipeline
- Deep-dive into the [Rule Engine](../components/rule-engine.md)
- Check the [Configuration](configuration.md) reference
