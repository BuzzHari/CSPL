# NET-005 — Random Early Detection Gateways for Congestion Avoidance

- **Title:** Random Early Detection Gateways for Congestion Avoidance
- **Authors:** Sally Floyd; Van Jacobson
- **Year:** 1993
- **Field:** Computer Networking / Active Queue Management / Congestion Avoidance / Queue Management
- **Status:** Queued
- **Priority:** Core
- **Date recommended:** 2026-09-18
- **Primary source:** https://www.icir.org/floyd/papers/early.pdf
- **DOI:** https://doi.org/10.1109/90.251892

## Why this paper matters

TCP congestion control can react only after the network provides a congestion signal. With simple Drop Tail queues, that signal often arrives only after a queue has filled and packets are dropped. Large queues can therefore remain persistently full, increasing latency, and synchronized losses can cause many TCP senders to reduce their windows at the same time.

Floyd and Jacobson introduced Random Early Detection (RED), one of the foundational active queue management algorithms. RED moves the gateway from passive overflow handling to **early congestion detection and probabilistic signalling**. It tracks an exponentially weighted moving average of queue occupancy and begins randomly marking or dropping packets before the queue is full.

The important systems idea is broader than the particular RED parameterization: a queue should not merely store packets until it overflows. It can be an active control point that detects sustained congestion, distinguishes it from short bursts, and feeds information back to adaptive endpoints before hard resource exhaustion occurs.

RED strongly influenced later active queue management work and the evolution toward explicit congestion notification. Its original tuning can be difficult in practice, and newer AQMs such as CoDel and PIE address different problems, but RED remains a canonical paper for understanding why queue management is part of congestion control rather than merely buffer management.

## Prerequisites

- Basic TCP congestion control: congestion window, slow start, congestion avoidance, retransmission after loss.
- Queues, bottleneck links, queueing delay, and buffer overflow.
- Delay-bandwidth product and bursty traffic.
- Basic probability and exponentially weighted moving averages.
- A rough understanding of why several TCP flows simultaneously reducing their windows can reduce link utilization.

## Core mechanism

RED maintains an average queue size rather than reacting directly to the instantaneous queue length. Conceptually:

```text
packet arrives
     |
     v
update average queue size (EWMA)
     |
     +-- avg < min_th ----------------> enqueue normally
     |
     +-- min_th <= avg < max_th ------> mark/drop probabilistically
     |
     `-- avg >= max_th ----------------> mark/drop every arrival
```

For the middle region, the base marking probability grows approximately linearly with the average queue size:

```text
p_b = max_p * (avg - min_th) / (max_th - min_th)
```

RED then adjusts this probability according to the number of packets since the previous mark so marks are distributed more evenly rather than clustering accidentally.

The algorithm deliberately separates two questions:

1. **Is persistent congestion developing?** — estimated from the filtered average queue size.
2. **Which arrivals should receive congestion signals?** — selected probabilistically.

That separation is one of the paper's most important design ideas.

## Section-by-section reading guide

### 1. Introduction — read fully

Start from the problem the authors are trying to solve: high throughput should not require keeping very large queues full. Notice their argument that a gateway has information an individual sender does not: it sees aggregate queue behaviour across flows and can distinguish persistent queueing from ordinary propagation delay more directly.

Also note the deployment constraint. RED is designed to work with adaptive transports such as TCP and can signal congestion either by dropping a packet or, where the protocol supports it, by marking a packet.

### 2. Previous work on congestion-avoidance gateways — read selectively

Understand the contrast with Drop Tail, Random Drop, Early Random Drop, and DECbit. You do not need to memorize the older algorithms. The useful question is why simply waiting for buffer exhaustion, or using a fixed threshold/probability, can produce synchronization, bias, or poor responsiveness.

### 3. Design guidelines — read very carefully

This section contains the conceptual requirements for RED:

- keep average queue size low while tolerating short bursts;
- detect incipient congestion before overflow;
- avoid global synchronization of many TCP flows;
- avoid systematic bias against bursty traffic;
- avoid requiring per-flow state for ordinary operation;
- retain an upper bound on sustained queue occupancy even if sources do not cooperate.

Treat these as the specification from which the algorithm is derived.

### 4. The RED algorithm — read line by line

This is the core section. Follow the roles of `w_q`, `min_th`, `max_th`, `max_p`, `avg`, and `count`.

The EWMA makes RED intentionally insensitive to short queue spikes while still responding to persistent pressure. Between the two thresholds, the mark/drop probability increases with congestion. Above the maximum threshold, every arrival is signalled.

The `count` adjustment matters because independent fixed-probability marking can generate long gaps or clusters of marks. RED reshapes the spacing of signals to reduce this undesirable randomness.

### 5. A simple simulation — read once

Use the simulations to connect the mechanism to TCP's window dynamics. Do not memorize topology dimensions or parameter values. Observe how queue feedback alters sender behaviour before continuous queue overflow.

### 6. Calculating the average queue size — read carefully, skim derivations on the first pass

This section explains the control-loop timescale. If `w_q` is too high, RED reacts to transient bursts that should have been absorbed by the queue. If it is too low, the average responds too slowly and congestion can grow before RED notices it.

This is a general lesson in telemetry-driven control: **the smoothing timescale is part of the algorithm's semantics**, not merely a cosmetic metric setting.

### 7. Calculating the packet-marking probability — read carefully

Understand why the authors do more than apply a raw independent probability on each arrival. The final marking rule attempts to spread congestion indications more evenly in packet space, reducing the chance of both long unmarked runs and clustered marks.

### 8. Evaluation of RED gateways — read for claims, not constants

Evaluate RED against the requirements from Section 3: congestion avoidance, efficiency, fairness-related behaviour, robustness to traffic variation, and parameter sensitivity. Separate what the simulations demonstrate from what remains dependent on workload and tuning.

### 9. Bursty traffic — read fully

This section is important because instantaneous queue occupancy is not equivalent to congestion. A short burst may temporarily create a queue even when the long-term offered load is sustainable. RED's averaging is meant to absorb such bursts instead of penalizing them immediately.

### 10. Identifying misbehaving users — skim

RED is principally an aggregate queue-management mechanism, not a complete per-flow fairness system. The discussion exposes the boundary between stateless aggregate signalling and mechanisms that identify or police specific high-bandwidth users.

### 11. Implementation — read fully

Pay attention to the practical concern of making queue management cheap enough for the forwarding path. The algorithm was designed with constant per-packet state and without requiring ordinary per-flow state, which matters for scalable router implementation.

### 12. Conclusions and future work — read fully

Revisit the paper's main decomposition: detect persistent congestion using queue history, then signal endpoints probabilistically before hard buffer exhaustion. Note the open questions around selecting the desired average queue size and robust parameter settings; these foreshadowed decades of subsequent AQM research.

## Five key ideas

1. **Congestion should be signalled before the queue is full.** Buffer overflow is a late congestion signal and can create both high delay and synchronized loss.

2. **Instantaneous queue length and persistent congestion are different.** An EWMA lets the gateway tolerate short bursts while reacting to sustained pressure.

3. **Congestion detection and congestion signalling should be separate mechanisms.** RED first estimates whether congestion exists, then independently selects which packet arrivals receive signals.

4. **Randomization prevents synchronization.** Probabilistic marking helps keep many adaptive TCP flows from all backing off simultaneously after one overflow episode.

5. **Queue management participates in the end-to-end control loop.** Router queues are not merely storage; their behaviour changes transport dynamics, latency, throughput, and fairness.

## Connection to Linux and Aruba datapath engineering

This paper is directly relevant to packet forwarding and QoS work. Consider an egress queue on a gateway or AP:

```text
many client flows
       |
       v
classification / QoS
       |
       v
   egress queue
       |
       v
 physical link
```

A pure tail-drop implementation answers only one question: *is the queue out of space?* By the time the answer is yes, the system has already accumulated maximum queueing delay.

RED instead asks a more operationally useful question: *is sustained demand beginning to exceed service capacity?* That is similar to how a datapath diagnostic should distinguish a short-lived spike from a persistent failure mode.

For Aruba-style wireless or gateway debugging, this distinction matters when a complaint presents as "packet loss" or "high latency." Evidence worth correlating includes:

```text
instantaneous queue depth
filtered / historical queue depth
packet drops or ECN marks
per-traffic-class occupancy
link service rate
TCP retransmissions
client airtime / wireless contention
scheduler decisions
```

Two systems can have the same instantaneous queue depth but very different histories: one may be absorbing a legitimate microburst while the other has been persistently congested for seconds. RED's design makes the history explicit.

The implementation lesson is also useful for high-rate Linux datapaths. A control mechanism on the hot path must minimize state and per-packet cost. RED's aggregate per-queue state is an example of trading some precision for a scalable implementation. Modern Linux qdiscs use more recent AQM and fair-queueing mechanisms, but the design question remains the same: **how much per-packet/per-flow state can the datapath afford, and what feedback signal gives endpoints enough information to adapt before latency explodes?**

## What to remember after reading

If only one idea remains, make it this: **a full queue is not the first moment congestion exists; it is the moment an earlier control opportunity has already been missed.**

That insight links RED directly to modern active queue management, ECN, latency-sensitive networking, and feedback-driven systems design.

## Related papers in this library

- NET-003 — Congestion Avoidance and Control
- NET-004 — The Design Philosophy of the DARPA Internet Protocols
- NET-002 — A Protocol for Packet Network Intercommunication
- ARCH-001 — End-to-End Arguments in System Design
