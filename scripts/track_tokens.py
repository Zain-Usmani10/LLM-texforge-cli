import os
import glob
import json

def get_session_log_files():
    base_path = os.path.expanduser(r"~\.claude\projects")
    search_pattern = os.path.join(base_path, "*", "*.jsonl")
    return glob.glob(search_pattern)

def parse_telemetry(file_paths):
    metrics = {
        "input_tokens": 0,
        "cache_read": 0,
        "cache_creation": 0,
        "output_tokens": 0,
        "thinking_tokens": 0
    }
    
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    usage = event.get("usage") or event.get("message", {}).get("usage")
                    if usage:
                        metrics["input_tokens"] += usage.get("input_tokens", 0)
                        metrics["cache_read"] += usage.get("cache_read_input_tokens", 0)
                        metrics["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
                        metrics["output_tokens"] += usage.get("output_tokens", 0)
                        
                        output_details = usage.get("output_tokens_details")
                        if output_details:
                            metrics["thinking_tokens"] += output_details.get("thinking_tokens", 0)
                except json.JSONDecodeError:
                    continue
    return metrics

def render_bar(count, max_val, max_width=25):
    if max_val == 0:
        return ""
    bar_len = int((count / max_val) * max_width)
    return "█" * bar_len

def main():
    log_files = get_session_log_files()
    if not log_files:
        print("No Claude telemetry logs found.")
        return
        
    metrics = parse_telemetry(log_files)
    payload_tokens = max(0, metrics["output_tokens"] - metrics["thinking_tokens"])
    
    categories = [
        ("Input (Fresh)", metrics["input_tokens"]),
        ("Cache Write", metrics["cache_creation"]),
        ("Cache Read", metrics["cache_read"]),
        ("LaTeX Payload", payload_tokens),
        ("Thinking", metrics["thinking_tokens"]),
    ]
    
    max_count = max(c[1] for c in categories) or 1
    total_tokens = sum(c[1] for c in categories)

    print("\n" + "=" * 68)
    print(f"{'CLAUDE TELEMETRY & TOKEN DISTRIBUTION':^68}")
    print("=" * 68)
    print(f"{'Category':<16} | {'Count':>10} | {'Visual Ratio':<26}")
    print("-" * 68)
    for name, count in categories:
        bar = render_bar(count, max_count)
        print(f"{name:<16} | {count:>10,} | {bar:<26}")
    print("-" * 68)
    print(f"{'TOTAL PROCESSED':<16} | {total_tokens:>10,} |")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    main()