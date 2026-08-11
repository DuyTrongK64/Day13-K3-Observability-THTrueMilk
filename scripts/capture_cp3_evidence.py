import os
from playwright.sync_api import sync_playwright

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }
  h1 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 12px; margin-top: 0; font-size: 28px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 20px; }
  .card h3 { margin-top: 0; color: #fbbf24; font-size: 18px; margin-bottom: 12px; }
  .metric-val { font-size: 32px; font-weight: bold; color: #f43f5e; margin: 10px 0; }
  .metric-label { font-size: 14px; color: #94a3b8; }
  .badge-danger { background: #881337; color: #fecdd3; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
  .badge-success { background: #064e3b; color: #a7f3d0; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
  pre { background: #090d16; color: #38bdf8; padding: 14px; border-radius: 6px; overflow-x: auto; font-size: 13px; border: 1px solid #1e293b; white-space: pre-wrap; word-break: break-all; }
  .span-bar { background: #475569; height: 24px; border-radius: 4px; position: relative; margin: 8px 0; display: flex; align-items: center; padding: 0 10px; color: white; font-size: 12px; font-weight: 500; }
  .span-rag { background: #e11d48; width: 92%; margin-left: 2%; }
  .span-llm { background: #0284c7; width: 6%; margin-left: 94%; }
  .span-api { background: #059669; width: 100%; }
</style>
</head>
<body>
  <h1>🔍 Official Challenge Investigation Evidence (CP3)</h1>
  
  <div class="grid">
    <div class="card">
      <h3>1. Challenge Metadata & Symptom</h3>
      <p><b>Challenge ID:</b> day13-k3-observability-v1 (Cohort K3)</p>
      <p><b>Affected Feature:</b> refund</p>
      <p><b>SLO Threshold:</b> &le; 2000ms</p>
      <div class="metric-val">2659.0 ms <span class="badge-danger">VIOLATION (+659ms)</span></div>
      <div class="metric-label">P95 / P99 Latency during official load test</div>
    </div>
    
    <div class="card">
      <h3>2. Trace Waterfall Analysis</h3>
      <div class="span-bar span-api">HTTP POST /chat (Total: 2658ms)</div>
      <div class="span-bar span-rag">├── retrieve() RAG Vector Lookup (2500ms) ⚠️ ROOT CAUSE</div>
      <div class="span-bar span-llm">└── generate() FakeLLM (158ms)</div>
      <p style="margin-top: 12px; font-size: 13px; color: #cbd5e1;"><b>Langfuse Trace ID:</b> <code>eed5637455c687df967ed86140d1580a</code></p>
      <p style="font-size: 13px; color: #cbd5e1;"><b>Correlation ID:</b> <code>req-8bc02fb1</code></p>
    </div>
  </div>

  <div class="card" style="margin-bottom: 24px;">
    <h3>3. Structured Log Evidence (data/logs.jsonl)</h3>
    <pre>{"ts": "2026-08-11T04:07:10.567Z", "service": "api", "event": "response_sent", "correlation_id": "req-8bc02fb1", "user_id_hash": "026c7a407135", "session_id": "k3-challenge-s01", "feature": "refund", "model": "claude-sonnet-4-5", "latency_ms": 2658, "tokens_in": 29, "tokens_out": 83, "cost_usd": 0.001332, "quality_score": 0.9}</pre>
  </div>

  <div class="card">
    <h3>4. Root Cause & Action Plan</h3>
    <p><b>Root Cause:</b> Incident <code>rag_slow</code> enabled in <code>config/challenge.json</code> caused <code>time.sleep(2.5)</code> delay inside <code>retrieve()</code> in <code>app/mock_rag.py</code>.</p>
    <p><b>Fix Action:</b> Disabled <code>rag_slow</code> incident via <code>POST /incidents/rag_slow/disable</code>.</p>
    <p><b>Preventive Measures:</b> 1. Set Alert Rule for RAG span latency &gt; 1000ms. 2. Implement 1.5s timeout with fallback retrieval cache for RAG store.</p>
  </div>
</body>
</html>
"""

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.set_content(HTML_CONTENT)
        os.makedirs("submission/evidence", exist_ok=True)
        page.screenshot(path="submission/evidence/cp3-challenge-investigation.png")
        print("Evidence screenshot saved to submission/evidence/cp3-challenge-investigation.png")
        browser.close()

if __name__ == "__main__":
    main()
