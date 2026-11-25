# Ryan J. Hamby

Software engineer, New York, NY. ryan.j.hamby@gmail.com · https://ryanjhamby.dev · https://github.com/RyanJHamby · https://www.linkedin.com/in/ryan-j-hamby/

I make AI compute fast, efficient, and reliable, from the serving layer down to the hardware and the power behind it.

Every number below comes from the site's own pages; captured runs and their hardware are listed at https://ryanjhamby.dev/receipts/ (machine-readable: https://ryanjhamby.dev/claims.json).

## Experience

### Senior Software Engineer, inference data plane
AI company (not named here yet) · Nov 2026 – Present · New York, NY

### Software Development Engineer II, Amazon Web Services
AWS Marketplace, Payment Compliance Team · Dec 2024 – Nov 2026 · New York, NY

- Owned dual-partition, multi-tenant infrastructure upgrades with cross-partition DynamoDB replication, enabling AWS Marketplace expansion into the EU sovereign cloud and supporting $112M+/yr in new GMV.
- Led pre-launch compliance review identifying 7 regulatory gaps (GDPR, PCI-DSS, KYC) across EU/APAC that would have blocked a $100M+ annual revenue stream.
- Built an event-driven sync service guaranteeing exactly-once delivery via SQS FIFO and DynamoDB conditional writes across 3 payment workflows, eliminating $2M+/yr in reconciliation errors.
- Led build of the Payment Adapter Service (parallel third-party verification, circuit breakers, idempotent retries, async callbacks), reducing Japanese seller onboarding from 6 days to 5 minutes and unlocking $10M+/yr in sales.

### Software Development Engineer, Amazon Web Services
AWS IoT SiteWise / AWS Marketplace · Mar 2023 – Nov 2024 · Boston, MA / New York, NY

- Redesigned the AWS IoT SiteWise asset hierarchy, reducing customer onboarding by 40% and enabling 10K+ concurrent industrial IoT devices per account.
- Eliminated UUID collision vulnerabilities affecting 3 high-traffic APIs with token-based idempotency (3-hour expiration windows), preventing duplicate resource creation in systems processing 1M+ requests/day.
- Replaced a coarse synchronized block with a lock-striped ConcurrentHashMap dedup index in the SiteWise Java control plane, unblocking 10K+ concurrent writes.
- First engineer on the new AWS IoT SiteWise Boston team; onboarded 7 engineers to production in 30 days.
- Shipped: AWS IoT SiteWise Bulk Import/Export; User-Defined Unique Identifiers.

## Upstream contributions

- vLLM (merged 2026-08-03): fixed a StopIteration crash in Qwen3-Omni multimodal processing on videos with no audio track when use_audio_in_video=True, plus two follow-on false-positive paths in processor caching. https://github.com/vllm-project/vllm/pull/48420
- Firecracker (merged 2026-07-16): fixed a VMM panic on ACPI device restore when EventFd creation fails under fd exhaustion. https://github.com/firecracker-microvm/firecracker/pull/6032
- Firecracker (merged 2026-07-23, docs): documented the cause of a DNS lookup delay from an IPv6 resolver stall. https://github.com/firecracker-microvm/firecracker/pull/6033

## Selected work

- FlowState (Rust + Python, Arrow): Rust-kernel temporal join engine with a Python API for point-in-time ML feature pipelines, batch and streaming, zero-copy Arrow.
- GPU Flight Recorder (Go, gRPC): names the straggling rank in distributed GPU training by joining NCCL collective timings with per-GPU telemetry. Validated in simulation; no real-hardware results yet.
- Low-Latency Order Book Engine (C++20): lock-free SPSC ingestion and thread-local slab pools, benchmarked on EC2.
- autopilot-kit (GitHub Actions, Python): guardrails for running coding agents across repos; reusable workflows and stdlib scripts pinned by commit SHA.
- Zonevex (Python, PostGIS; paused Nov 2026): checked whether a developer's site control would hold up against interconnection-queue rules. Postmortem: https://ryanjhamby.dev/writing/zonevex-retrospective/

## Education

University of Michigan · B.S.E. in Computer Science, Minor in Electrical Engineering · Dec 2022 · GPA 3.65/4.00, Magna Cum Laude

## Certifications

- AWS Certified Solutions Architect Associate (2024)
- AWS Certified Developer (2025)

## Skills

- Languages: Rust, C++ (C++20), Python, Java (strong) | Go, TypeScript, SQL (familiar)
- ML / GPU systems: vLLM (contributor), PyTorch Distributed (DDP), NCCL, NVML, KV cache, CUDA Graphs
- Systems and performance: concurrency, lock-free data structures, memory ordering, profiling (perf), ThreadSanitizer, Apache Arrow
- Distributed systems: Kafka, gRPC/Protobuf, exactly-once delivery, idempotency, circuit breakers, stream processing
- Cloud and infra: AWS, Linux, Docker, Redis, PostgreSQL, Prometheus, CI/CD
