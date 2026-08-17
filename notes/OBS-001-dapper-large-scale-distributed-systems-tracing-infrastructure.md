# OBS-001 — Dapper, a Large-Scale Distributed Systems Tracing Infrastructure

- **Authors:** Benjamin H. Sigelman, Luiz André Barroso, Mike Burrows, Pat Stephenson, Manoj Plakal, Donald Beaver, Saul Jaspan, Chandan Shanbhag
- **Year:** 2010
- **Field:** Observability / Distributed Tracing / Distributed Systems
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/

## Why it matters

Dapper is the landmark production distributed-tracing paper. It showed how to make end-to-end request tracing practical across a very large, heterogeneous service fleet by combining trace-context propagation, low-overhead instrumentation in common RPC/threading libraries, sampling, centralized trace collection, and reusable analysis tooling.

The paper's lasting contribution is architectural rather than tied to one Google implementation: tracing becomes a platform capability when correlation identifiers and timing metadata are propagated automatically through common infrastructure rather than requiring every application team to hand-instrument every request path.

Dapper directly influenced later distributed-tracing systems and standards, including the span/trace model now familiar from systems such as Zipkin, Jaeger, OpenTracing, and OpenTelemetry.

## Prerequisites

- Basic distributed systems and RPCs
- Client/server request flows
- Latency and tail-latency concepts
- Logs, metrics, and tracing at a conceptual level
- Sampling and basic probability intuition
- Familiarity with service dependencies is helpful but not required

## Key ideas

1. **Trace requests end-to-end with shared context** — a trace identifier connects work performed by many processes and machines into one causal request graph.
2. **Make instrumentation transparent and ubiquitous** — instrument common RPC, threading, and control-flow libraries so application teams get tracing with minimal code changes.
3. **Represent work as spans** — each unit of work records parent/child relationships, timing, and annotations, producing a distributed call tree rather than isolated log lines.
4. **Control cost with sampling** — always-on tracing can be operationally viable when only a fraction of requests are retained while instrumentation overhead remains low.
5. **Treat tracing as a platform, not one UI** — once trace data is available centrally, many debugging, latency-analysis, dependency, and monitoring tools can be built on the same substrate.

## Recommended reading approach

**Read fully.** The paper is relatively compact and its production lessons are as important as the tracing data model.

### Section-by-section guide

- **Introduction:** Understand the three design goals: low overhead, application-level transparency, and ubiquitous deployment at large scale.
- **Distributed tracing in Dapper:** Read carefully. Learn the trace/span model, parent-child relationships, annotations, and how trace context follows a request across process boundaries.
- **Instrumentation:** Focus on why common libraries are the leverage point. The architectural insight is to capture causality at shared infrastructure boundaries rather than depending on every service owner.
- **Collection and storage:** Understand the path from local trace records to centralized storage, and note the distinction between instrumentation cost and retained-data volume.
- **Sampling:** Read closely. Sampling is what lets a production tracer remain continuously enabled without recording every request.
- **Trace search and analysis:** Observe how the same trace substrate supports latency diagnosis, dependency analysis, and developer-facing tools.
- **Production experience / use cases:** Do not skip. These sections explain which design choices actually mattered after deployment and how Dapper evolved from a tracing tool into a monitoring platform.
- **Discussion / lessons:** Revisit the trade-offs around completeness, overhead, transparency, and the limits of sampled traces.

## Estimated reading time

- Focused first read: 50–70 minutes
- With architecture notes and comparison to OpenTelemetry: 90–120 minutes

## Practical connection to Linux and Aruba networking work

Dapper's central problem is very similar to debugging a client operation that crosses several Aruba/Linux components. A roam, authentication event, configuration change, or packet-flow failure may involve an AP, gateway control plane, datapath process, authentication service, kernel/network stack, and external services.

Independent timestamps and logs answer only "what did each component print?" A Dapper-style trace answers a stronger question: "which pieces of work belonged to this one operation, and what caused what?"

For an Aruba observability architecture, a useful equivalent would propagate a stable operation context such as a client lifecycle ID, request ID, or trace ID across component boundaries and emit spans for meaningful stages:

```text
FT roam request
  ├─ AP processing
  ├─ gateway client-state update
  ├─ authentication / role update
  ├─ bridge/datapath programming
  └─ forwarding verification
```

That makes it possible to distinguish a slow stage, a missing stage, duplicated work, or an unexpected dependency without relying solely on timestamp-sorted logs. eBPF can complement this by producing kernel- or process-level spans/events at boundaries that applications cannot easily instrument.

## Questions to answer after reading

1. Why is transparent instrumentation in common libraries more scalable than asking every service team to add tracing manually?
2. What information does a span contain that an ordinary log line usually does not?
3. Which conclusions remain safe when traces are sampled, and which become statistically difficult?
4. Why did Dapper evolve into a platform for multiple tools rather than remain a single trace viewer?
5. In a network appliance, which boundaries are the equivalent of RPC boundaries where trace context should be propagated?

## Related indexed papers

- DS-003 — Time, Clocks, and the Ordering of Events in a Distributed System
- ARCH-001 — End-to-End Arguments in System Design
- DBG-001 — Eraser: A Dynamic Data Race Detector for Multithreaded Programs
- EBPF-001 — The BSD Packet Filter: A New Architecture for User-level Packet Capture
