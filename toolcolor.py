def change_color(color):
    # UI ko color dena
    return f"Color changed to {color}"


TOOL_MAP={
    "change_color": change_color
}

TOOLS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "change_color",
        "description": "Change the UI background color.",
        "parameters": {
            "type": "object",
            "properties": {
                "color": {
                    "type": "string",
                    "description": "The color to set, e.g. red, blue, green"
                }
            },
            "required": ["color"]
        }
    }
}