# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`:
- Tổng số traces:
- Số PII leak còn lại:
- Link/đường dẫn dashboard:

## 3. Logging và tracing

- Evidence correlation ID:
- Evidence PII redaction:
- Evidence trace waterfall:
- Giải thích một span đáng chú ý:

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: `v1` / `baseline`
- Version/label candidate: `v2` / `candidate`
- Trace ID của mỗi version:
  - Trace ID (v1 / production): `eed5637455c687df967ed86140d1580a`
  - Trace ID (v2 / candidate): `(Điền thêm ID của trace candidate từ danh sách bên trái)`
- Bằng chứng đổi label hoặc rollback: ![Rollback Evidence](evidence/cp2-rollback.png)

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ: 6/6 panel có trong dashboard contract.
- Evidence dashboard: ![Dashboard](evidence/cp2-dashboard.png)
- SLO đã chọn và lý do: Threshold p95 latency <= 3000ms để đảm bảo trải nghiệm real-time của Chatbot, Error Rate <= 2% để đảm bảo RAG không bị lỗi.
- Alert rules và runbook: Khi P95 > 3000ms, alert trigger. Runbook: Kiểm tra DB vector search duration hoặc tải của LLM endpoint.

## 6. Điều tra challenge

- Challenge ID:
- Triệu chứng từ metrics:
- Trace ID liên quan:
- Log line/correlation ID liên quan:
- Root cause:
- Fix action:
- Preventive measure:

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| | | | |
