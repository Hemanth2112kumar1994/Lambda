#AWS Lambda EBS Snapshot Automation & Monitoring

This project consists of two AWS Lambda functions designed to automate and monitor EBS (Elastic Block Store) volume snapshots using Python (boto3), CloudWatch, EventBridge, and S3.

---
##  Project Components

### `SnapshotCreatorFunction` – Scheduled/Manual EBS Snapshot Creation
Creates EBS snapshots for all volumes (or filtered volumes by tag) and stores creation logs in an S3 bucket.

- ✅ Tags snapshots automatically
- ✅ Logs all snapshot activity
- ✅ Saves logs to `S3:///Snapshot-creation/`
- ✅ Supports CloudWatch scheduled triggers or manual execution

### 2️⃣ `SnapshotMonitorFunction` – Snapshot Monitor and Cleanup
Triggered by CloudWatch Events when a new snapshot is created, or run manually to list and optionally delete old snapshots.

- ✅ Captures `snapshot_id`, `volume_id`, and timestamp
- ✅ Uploads logs to `S3://logs/`
- ✅ Supports manual trigger or EventBridge integration
- ✅ Conditional cleanup logic (toggle via env var `DELETE_SNAPSHOTS`)

---
## 📈 Business Value

### 🔐 Data Protection & Backup Strategy
This setup enforces snapshot-based backups, helping your organization:
- Achieve **disaster recovery compliance**
- Maintain **data integrity** with consistent backups
- Automate **snapshot lifecycle management** (creation & cleanup)

### 💰 Cost Optimization
- Prevents accumulation of unnecessary snapshots
- Allows fine-tuned control over snapshot retention via tagging or scheduling
- Avoids manual snapshot management across multiple volumes


