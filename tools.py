import psutil

# 1. Actual Python Execution Functions
def get_cpu_usage():
    """System ki current CPU usage % return karta hai."""
    usage = psutil.cpu_percent(interval=1)
    return f"Current CPU usage is {usage}%"

# Map function names (strings) to actual Python callable functions
TOOL_MAP = {
    "get_cpu_usage": get_cpu_usage
}

# 2. Tool Schema Definitions (Model ke samajhne ke liye)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_cpu_usage",
            "description": "Get the current CPU usage of the server.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]