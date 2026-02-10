# 03 — MVP Build Plan (Individual-Friendly)

## Scope for hackathon
Build one complete “golden path”:
1. Import sample legacy app.
2. Run analysis + migration plan.
3. Apply one meaningful automated migration.
4. Run validation checks.
5. Deploy migrated app to GCP Cloud Run.

## 14-day execution plan

### Day 1–2: Foundation
- Set repo structure and architecture docs.
- Setup API skeleton + database schema.
- Setup CI with lint and tests.

### Day 3–5: Ingestion + Analysis
- Implement repo ingestion flow.
- Extract dependency and framework metadata.
- Generate risk/complexity report.

### Day 6–8: Strategy + Transformation
- Implement migration planner with risk scoring.
- Implement one production-grade transformer (e.g., config externalization + Dockerization).
- Generate PR-ready patch output.

### Day 9–10: Validation + Security
- Add test runner integration.
- Add static analysis and dependency scanning.
- Build migration report dashboard payload.

### Day 11–12: UI + Demo polish
- Build simple but polished dashboard:
  - project status
  - migration plan
  - before/after metrics
- Add progress timeline and logs.

### Day 13: Deployment hardening
- Deploy on Cloud Run.
- Validate end-to-end flow with sample repo.
- Add rollback script and runbook.

### Day 14: Pitch + recording
- Rehearse 5–7 minute demo.
- Show business value, technical depth, and deployment readiness.

## MVP success metrics
- Time to produce migration plan: < 10 minutes for sample repo.
- Automated task success rate: > 80% on pre-scoped transformations.
- Deployment success: one-click pipeline to Cloud Run.
- Judge-friendly clarity: dashboard + report + live deploy.
