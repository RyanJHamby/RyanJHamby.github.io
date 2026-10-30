+++
title = "Experience"
+++

## Amazon Web Services - Software Development Engineer II

**AWS Marketplace, Payment Compliance Team | Dec 2024 - Present | New York, NY**

![Amazon Logo](/images/amazon.png)

### Key Achievements

<div class="achievement">
Owned dual-partition, multi-tenant infrastructure upgrades with cross-partition DynamoDB replication, enabling AWS Marketplace expansion into the EU sovereign cloud and supporting <span class="metric">$112M+/yr in new GMV</span>
</div>

<div class="achievement">
Led pre-launch compliance review identifying <span class="metric">7 regulatory gaps</span> (GDPR, PCI-DSS, KYC) across EU/APAC that would have blocked <span class="metric">$100M+ annual revenue stream</span>
</div>

<div class="achievement">
Built an event-driven sync service guaranteeing exactly-once delivery via SQS FIFO and DynamoDB conditional writes across 3 payment workflows, eliminating <span class="metric">$2M+/yr in reconciliation errors</span>
</div>

<div class="achievement">
Led build of the Payment Adapter Service (parallel third-party verification, circuit breakers, idempotent retries, async callbacks), reducing Japanese seller onboarding from <span class="metric">6 days to 5 minutes</span> and unlocking <span class="metric">$10M+/yr in sales</span>
</div>

---

## Amazon Web Services - Software Development Engineer

**AWS IoT SiteWise / AWS Marketplace | Mar 2023 - Nov 2024 | Boston, MA / New York, NY**

### Highlights

<div class="achievement">
Redesigned AWS IoT SiteWise asset hierarchy reducing customer onboarding by <span class="metric">40%</span> and enabling <span class="metric">10K+ concurrent industrial IoT devices</span> per account
</div>

<div class="achievement">
Eliminated UUID collision vulnerabilities affecting 3 high-traffic APIs by implementing token-based idempotency with 3-hour expiration windows, preventing duplicate resource creation in distributed systems processing <span class="metric">1M+ requests/day</span>
</div>

<div class="achievement">
Replaced a coarse synchronized block with a lock-striped ConcurrentHashMap dedup index in the SiteWise Java control plane, unblocking <span class="metric">10K+ concurrent writes</span>
</div>

<div class="achievement">
First engineer on the new AWS IoT SiteWise Boston team; onboarded 7 engineers to production in 30 days
</div>

### Featured Projects

- [AWS IoT SiteWise Bulk Import/Export](https://aws.amazon.com/about-aws/whats-new/2023/11/aws-iot-sitewise-support-bulk-import-export-update-metadata/?ref=dailydev)
- [User-Defined Unique Identifiers](https://aws.amazon.com/about-aws/whats-new/2023/11/aws-iot-sitewise-user-defined-unique-identifiers/)

![AWS SiteWise Bulk Import](/images/SiteWiseBulkImport.png)
