from src import get_sandbox

if __name__ == "__main__":
    # Get Docker sandbox with config
    sandbox = get_sandbox()
    
    # Run the agent in Docker
    print(f"Running agent in Docker container...")
    sandbox.run_command()
