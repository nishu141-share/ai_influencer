import sys
from agents.graph import create_agent_graph

def main():
    if len(sys.argv) < 2:
        print("Usage: python main_agent.py <topic>")
        sys.exit(1)
        
    topic = " ".join(sys.argv[1:])
    print(f"Starting AI Influencer Agent for topic: '{topic}'")
    
    app = create_agent_graph()
    
    # Initial state
    inputs = {"topic": topic}
    
    # Invoke the graph
    # We use stream to see steps
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Finished Node: {key}")
            if "error" in value:
                print(f"Error in {key}: {value['error']}")
                sys.exit(1)
                
    print("\nWorkflow Completed!")

if __name__ == "__main__":
    main()
