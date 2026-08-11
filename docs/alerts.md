# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: high_latency_p95
- Severity: critical
- SLI/SLO liên quan: Latency P95 <= 3000ms
- Điều kiện và thời gian duy trì: `latency_p95_ms > 3000` trong 5 phút
- Ảnh hưởng tới người dùng: Phản hồi từ chatbot AI bị trễ lớn, ảnh hưởng trải nghiệm người dùng cuối.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra Dashboard chỉ số Latency P95 và breakdown theo feature.
  2. Mở Langfuse Trace xem span waterfall của các request bị trễ (xác định do RAG vector search hay do LLM generate).
  3. Tra cứu `data/logs.jsonl` tìm correlation ID của các log event `response_sent` có `latency_ms` > 3000.
- Mitigation tạm thời: Tắt bớt incident/rào chắn nút nghẽn (hoặc bypass RAG retriever nếu vector store bị quá tải/sleep).
- Owner: oncall-team

## Alert 2

- Tên: high_error_rate
- Severity: critical
- SLI/SLO liên quan: Error Rate <= 2%
- Điều kiện và thời gian duy trì: `error_rate_pct > 2%` trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng nhận phản hồi HTTP 500 khi thực hiện yêu cầu chat.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel Error Rate và Error Breakdown trên Dashboard.
  2. Lọc log `event == "request_failed"` trong `data/logs.jsonl` để lấy `error_type` và `detail`.
  3. Mở Trace ID tương ứng trên Langfuse để kiểm tra exception ở span bị lỗi.
- Mitigation tạm thời: Khởi động lại service API hoặc bật cơ chế fallback thông báo lỗi thân thiện cho khách hàng.
- Owner: oncall-team

## Alert 3

- Tên: low_quality_score
- Severity: warning
- SLI/SLO liên quan: Quality Score Avg >= 0.75
- Điều kiện và thời gian duy trì: `quality_score_avg < 0.75` trong 15 phút
- Ảnh hưởng tới người dùng: Chất lượng câu trả lời của AI kém, bị mất thông tin hoặc chứa mã redacted sai ngữ cảnh.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel Quality Score trên Dashboard.
  2. Kiểm tra phiên bản Prompt đang áp dụng (`prompt_version`, `prompt_label`).
  3. Kiểm tra kết quả trả về của RAG context để đảm bảo không bị thiếu tài liệu tham khảo.
- Mitigation tạm thời: Rollback phiên bản prompt về `baseline` (v1) hoạt động ổn định.
- Owner: ai-engineers
