from src import loader

if __name__ == "__main__":
    # Get Docker sandbox with config
    sandbox = loader.sandbox
    
    # Run the agent in Docker
    print(f"Running agent in Docker container...")
    sandbox.run_command()
