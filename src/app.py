"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import ast
import json
import os
import re
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return None

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from prompts import CHATBOT_BASELINE_PROMPT, MAX_ITERATIONS, REACT_SYSTEM_PROMPT
from providers import get_llm_provider
from tools import AVAILABLE_TOOLS

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """Dựng Chatbot gốc (Baseline) không có công cụ."""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def _parse_action(text: str):
    match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\[(.*)\]", text)
    if not match:
        return None, None
    tool_name = match.group(1)
    raw_args = match.group(2).strip()
    if not raw_args:
        return tool_name, []
    try:
        parsed = ast.literal_eval(f"[{raw_args}]")
        return tool_name, parsed
    except Exception:
        return tool_name, [raw_args]


def _call_tool(tool_name: str, args):
    tool = AVAILABLE_TOOLS.get(tool_name)
    if not tool:
        return f"LỖI: Tool '{tool_name}' không tồn tại."
    try:
        if isinstance(args, list):
            return tool(*args)
        return tool(args)
    except TypeError:
        return f"LỖI: Sai tham số khi gọi tool '{tool_name}'."
    except Exception as exc:
        return f"LỖI: Tool '{tool_name}' gặp lỗi: {exc}"


def run_react_agent(user_query: str, provider):
    """Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails."""
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    context = f"{REACT_SYSTEM_PROMPT}\n\nUser: {user_query}"

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        response = provider.generate(context, system_prompt=REACT_SYSTEM_PROMPT)
        print(response)

        tool_name, args = _parse_action(response)
        if not tool_name:
            print("🛡️ GUARDRAIL: Không parse được Action hợp lệ, dừng an toàn.")
            break

        observation = _call_tool(tool_name, args)
        print(f"👁️ Observation: {observation}")
        context += f"\n{response}\nObservation: {observation}"

        if "Final Answer:" in response:
            break

    else:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước.")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")

    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")

    sample_query = tests[0]["question"]

    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)

    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)
