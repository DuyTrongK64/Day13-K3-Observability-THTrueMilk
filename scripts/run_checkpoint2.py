from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from langfuse import Langfuse

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Load environment variables
load_dotenv()

def main():
    print("Khởi tạo Langfuse Client...")
    langfuse = Langfuse()
    
    print("\n1. Tạo Prompt v1 (baseline, production)...")
    try:
        langfuse.create_prompt(
            name="day13-chat",
            type="text",
            prompt="Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}",
            labels=["baseline", "production"]
        )
        print("Đã tạo v1.")
    except Exception as e:
        print(f"Lỗi khi tạo v1: {e}")

    time.sleep(2)

    print("\n2. Tạo Prompt v2 (candidate)...")
    try:
        langfuse.create_prompt(
            name="day13-chat",
            type="text",
            prompt="Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}\nVui lòng trả lời ngắn gọn.",
            labels=["candidate"]
        )
        print("Đã tạo v2.")
    except Exception as e:
        print(f"Lỗi khi tạo v2: {e}")

    print("\n3. Gửi request với label 'baseline'...")
    os.environ["LANGFUSE_PROMPT_LABEL"] = "baseline"
    from app.agent import LabAgent
    agent = LabAgent()
    res1 = agent.run(
        user_id="user_123",
        feature="qa",
        session_id="sess_1",
        message="What is observability?"
    )
    print("Xong request baseline.")

    print("\n4. Gửi request với label 'candidate'...")
    os.environ["LANGFUSE_PROMPT_LABEL"] = "candidate"
    res2 = agent.run(
        user_id="user_123",
        feature="qa",
        session_id="sess_2",
        message="What is observability?"
    )
    print("Xong request candidate.")
    
    print("\n5. Thử nghiệm đổi label production sang v2...")
    # Thay đổi label production sang v2, Langfuse SDK cho phép tạo lại hoặc dùng UI.
    # Trong script này, ta gọi request với production để tạo trace. (Lúc này production đang là v1)
    os.environ["LANGFUSE_PROMPT_LABEL"] = "production"
    res3 = agent.run(
        user_id="user_456",
        feature="qa",
        session_id="sess_3",
        message="How to monitor tail latency?"
    )
    print("Xong request production (v1).")

    langfuse.flush()
    print("\nHoàn tất tạo dữ liệu trace cho Prompt Versioning!")
    print("Vui lòng truy cập giao diện Langfuse để xem hai trace này, thao tác rollback label 'production' về v1, và chụp ảnh evidence.")

if __name__ == "__main__":
    main()
