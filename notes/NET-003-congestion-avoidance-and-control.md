# NET-003 — Congestion Avoidance and Control

- **Author:** Van Jacobson
- **Year:** 1988
- **Field:** Computer Networking / TCP / Congestion Control
- **Status:** Queued
- **Priority:** Core
- **Primary source:** https://ee.lbl.gov/www/papers/congavoid.pdf
- **Original publication:** ACM SIGCOMM 1988
- **DOI:** https://doi.org/10.1145/52324.52356

## Why it matters

This paper is one of the central works behind stable TCP operation on the Internet. After observing catastrophic congestion collapse, Jacobson developed a set of transport-side algorithms that made TCP adapt its sending rate to network conditions rather than blindly filling the receiver-advertised window.

The paper introduced or systematized mechanisms including slow start, round-trip-time variance estimation, exponential retransmission backoff, and dynamic congestion-window adjustment. Its broader contribution is a control-theoretic view of packet flow: a stable connection should obey a packet-conservation principle in which new packets are injected as old packets leave the network.

The LBL-hosted copy is a slightly revised version of the SIGCOMM 1988 paper and explicitly asks readers to cite the original SIGCOMM publication.

## Prerequisites

- TCP sliding windows and acknowledgements
- Round-trip time (RTT)
- Packet loss and retransmission
- Queues and bottleneck links
- Receiver flow control versus network congestion control
- Basic exponential backoff intuition

## Key ideas

1. **Packet conservation** — once a connection reaches equilibrium, acknowledgements effectively clock new packets into the network as old packets leave.
2. **Slow start** — a new or restarted flow should increase its congestion window gradually rather than inject a full receiver window immediately.
3. **Congestion window (`cwnd`)** — the sender needs a network-capacity limit distinct from the receiver's advertised flow-control window.
4. **Additive increase / multiplicative decrease** — increase cautiously while conditions are good, then reduce the sending window sharply after congestion is inferred.
5. **Better retransmission timing** — RTT variance and exponential timeout backoff are essential because poor timeout behavior can amplify congestion rather than recover from it.

## Recommended reading approach

**Read fully.** The paper is longer than some early networking classics, but the figures and empirical traces are part of the argument and are worth following.

### Introduction

Read fully. The motivating observation is extraordinary: throughput between LBL and UC Berkeley collapsed from tens of kilobits per second to tens of bits per second. Focus on why a transport implementation can destabilize the network even when the underlying protocol appears reasonable.

### Packet conservation and slow start

Read very carefully. This is the conceptual core. Understand the self-clocking behavior created by ACKs and why a connection that is not yet in equilibrium cannot safely assume the path can absorb a full window immediately.

### Round-trip timing and retransmission

Read carefully. Study why a single smoothed RTT estimate is insufficient and why variance matters when choosing retransmission timeouts. The important systems lesson is that premature retransmissions can create extra traffic exactly when the network is already overloaded.

### Congestion avoidance

Read fully. Follow the congestion-window adjustment logic and the reasoning behind additive increase and multiplicative decrease. The implementation is compact, but the stability argument matters more than memorizing the code.

### Experimental results

Do not skip the plots. Compare the behavior of old TCP implementations under congestion with the new algorithms. This is where the paper demonstrates that the control mechanisms restore useful throughput instead of merely looking plausible analytically.

### Gateway-side discussion

Read conceptually. Endpoint congestion control can keep offered load near network capacity, but endpoint algorithms alone cannot guarantee fair sharing among competing flows. This points toward later queue-management and scheduling work.

## Estimated reading time

- Focused first read: 60–90 minutes
- With figures, window traces, and a worked `cwnd` example: 2–3 hours

## Connection to Linux and Aruba networking work

This paper is directly relevant to datapath debugging because a packet drop is not just an isolated forwarding event; at transport level it can become feedback that changes the sender's future behavior.

When diagnosing poor client throughput through an Aruba AP or gateway, separate at least three layers of reasoning:

1. **Datapath behavior:** where are packets queued, dropped, reordered, or delayed?
2. **Transport inference:** does TCP interpret those observations as congestion, timeout, or loss?
3. **Control response:** how does `cwnd`, retransmission timing, and ACK pacing change afterward?

A short burst of drops can therefore produce a much longer throughput reduction even after the immediate datapath condition disappears. Packet captures combined with queue/drop telemetry and eBPF socket/TCP instrumentation can reveal whether the bottleneck is ongoing forwarding loss or the transport's recovery response to an earlier event.

The paper also provides a useful design principle for any feedback-controlled system: do not optimize only the instantaneous fast path. Ask whether local actions create a stable global control loop when many independent actors respond simultaneously.

## Questions to answer after reading

1. What is the packet-conservation principle, and why do ACKs create self-clocking?
2. Why is the receiver's advertised window insufficient as a congestion-control mechanism?
3. Why does slow start grow exponentially in time despite being described as "slow"?
4. Why can an inaccurate retransmission timer worsen congestion?
5. What behavior corresponds to additive increase and multiplicative decrease?
6. Why can endpoint congestion control improve stability without guaranteeing fairness?
7. During a throughput incident, how would you distinguish a current datapath bottleneck from TCP recovering from an earlier loss episode?

## Related indexed papers

- NET-002 — A Protocol for Packet Network Intercommunication
- ARCH-001 — End-to-End Arguments in System Design
- EBPF-001 — The BSD Packet Filter: A New Architecture for User-level Packet Capture
- NET-001 — The Click Modular Router
