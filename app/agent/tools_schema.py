#Tools are defined using JSON schema so the model understands parameter constraints.
def get_tool_definitions():
    return [
        {
            "name": "search_knowledge_base",
            "description": "Search internal documentation for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for the knowledge base"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of relevant chunks to retrieve"
                    },
                    "temprature": {
                        "type": "float",
                        "description": "temperature or precison for searching in the knowledge base"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_system_metrics",
            "description": "Retrieve current system metrics including CPU and memory usage.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    ]
