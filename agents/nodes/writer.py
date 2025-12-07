from agents.state import AgentState

def script_writer_node(state: AgentState) -> AgentState:
    """
    Generates a script based on the topic.
    TODO: Integrate Actual LLM here.
    """
    print(f"--> ScriptWriter working on topic: {state['topic']}")
    
    # Mock generation for initial testing
    topic = state['topic']
    script = f"Hello everyone! Today we are talking about {topic}. It is going to be amazing!"
    
    return {
        "script": script,
        "current_step": "script_written"
    }
