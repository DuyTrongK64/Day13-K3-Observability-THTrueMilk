import streamlit as st
import pandas as pd
import json
from pathlib import Path
import altair as alt

st.set_page_config(page_title="Day 13 AI Observability", layout="wide")
st.title("Day 13 AI Observability Dashboard")

log_path = Path("data/logs.jsonl")

@st.cache_data(ttl=30)
def load_data():
    if not log_path.exists():
        return pd.DataFrame(), pd.DataFrame()
    
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    events = [json.loads(line) for line in lines]
    df = pd.json_normalize(events)
    if df.empty:
        return df, df
        
    df['ts'] = pd.to_datetime(df['ts'])
    
    response_sent = df[df['event'] == 'response_sent'].copy()
    request_received = df[df['event'] == 'request_received'].copy()
    request_failed = df[df['event'] == 'request_failed'].copy()
    
    return df, response_sent, request_received, request_failed

df, response_sent, request_received, request_failed = load_data()

if df.empty:
    st.warning("No data found in data/logs.jsonl")
    st.stop()

# 1. Latency
st.header("1. Latency Percentiles (ms)")
if not response_sent.empty and 'payload.latency_ms' in response_sent.columns:
    p50 = response_sent['payload.latency_ms'].quantile(0.50)
    p95 = response_sent['payload.latency_ms'].quantile(0.95)
    p99 = response_sent['payload.latency_ms'].quantile(0.99)
    col1, col2, col3 = st.columns(3)
    col1.metric("P50", f"{p50:.1f} ms")
    col2.metric("P95", f"{p95:.1f} ms", delta="Threshold: <= 3000", delta_color="inverse" if p95 > 3000 else "normal")
    col3.metric("P99", f"{p99:.1f} ms")
    
    st.line_chart(response_sent.set_index('ts')['payload.latency_ms'])

# 2. Traffic
st.header("2. Request Traffic (req/min)")
if not request_received.empty:
    # aggregate by minute
    traffic = request_received.set_index('ts').resample('1min').size()
    total_reqs = len(request_received)
    col1, col2 = st.columns(2)
    col1.metric("Total Requests", total_reqs)
    rate = traffic.mean() if not traffic.empty else 0
    col2.metric("Avg Rate (req/min)", f"{rate:.2f}", delta="Threshold: >= 1", delta_color="normal" if rate >= 1 else "inverse")
    
    st.bar_chart(traffic)

# 3. Errors
st.header("3. Error Rate and Breakdown")
if not df.empty:
    total = len(request_received)
    errors = len(request_failed)
    error_rate = (errors / total * 100) if total > 0 else 0
    st.metric("Error Rate (%)", f"{error_rate:.2f}%", delta="Threshold: <= 2%", delta_color="inverse" if error_rate > 2 else "normal")
    
    if errors > 0 and 'payload.error_type' in request_failed.columns:
        error_counts = request_failed['payload.error_type'].value_counts()
        st.bar_chart(error_counts)

# 4. Cost
st.header("4. Cost over time (USD)")
if not response_sent.empty and 'payload.cost_usd' in response_sent.columns:
    total_cost = response_sent['payload.cost_usd'].sum()
    st.metric("Total Cost", f"${total_cost:.4f}", delta="Threshold: <= 2.5", delta_color="inverse" if total_cost > 2.5 else "normal")
    cost_series = response_sent.set_index('ts')['payload.cost_usd'].resample('1min').sum()
    st.line_chart(cost_series)

# 5. Tokens
st.header("5. Input and Output Tokens")
if not response_sent.empty and 'payload.tokens_in' in response_sent.columns and 'payload.tokens_out' in response_sent.columns:
    total_tokens_in = response_sent['payload.tokens_in'].sum()
    total_tokens_out = response_sent['payload.tokens_out'].sum()
    total_tokens = total_tokens_in + total_tokens_out
    col1, col2, col3 = st.columns(3)
    col1.metric("Tokens In", total_tokens_in)
    col2.metric("Tokens Out", total_tokens_out)
    col3.metric("Total Tokens", total_tokens, delta="Threshold: <= 50000", delta_color="inverse" if total_tokens > 50000 else "normal")

# 6. Quality
st.header("6. Quality Proxy")
if not response_sent.empty and 'payload.quality_score' in response_sent.columns:
    mean_quality = response_sent['payload.quality_score'].mean()
    st.metric("Mean Quality Score", f"{mean_quality:.2f}", delta="Threshold: >= 0.75", delta_color="normal" if mean_quality >= 0.75 else "inverse")
    st.line_chart(response_sent.set_index('ts')['payload.quality_score'])
