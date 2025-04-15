import subprocess
import os
import pathlib
from typing import List, Dict, Optional, Union


class SandboxProvider:
    """
    Provider class for sandbox functionality.
    Handles access to sandbox instances.
    """
    
    @staticmethod
    def get_sandbox(config: Dict):
        """
        Get a sandbox instance based on the provided configuration.
        
        Args:
            config: Dictionary containing sandbox configuration parameters
            
        Returns:
            Configured DockerSandbox instance
        """
        return DockerSandbox(config)


class DockerSandbox:
    """
    A class to manage running commands in a Docker sandbox environment.

    This class provides methods to build Docker images and run commands
    in Docker containers with appropriate configuration.
    """

    def __init__(self, config: Dict):
        """
        Initialize the Docker sandbox.

        Args:
            config: Docker configuration dictionary with settings for the sandbox
        """
        self.config = config
        self.image_name = config.get("image_name", "sandbox-image")
        self.dockerfile_path = config.get("dockerfile_path", ".")
        self.working_dir = config.get("working_dir", "/app")
        self.mount_path = os.getcwd()
        self.data_dir = config.get("data_dir", "/data")
        self.host_data_path = os.path.join(os.getcwd(), "data")
        
        # Ensure data directory exists
        pathlib.Path(self.host_data_path).mkdir(exist_ok=True)

    def rebuild_image(self) -> None:
        """Build or rebuild the Docker image using the Dockerfile."""
        print(f"Building Docker image {self.image_name}...")
        subprocess.run(["docker", "build", "-t", self.image_name, self.dockerfile_path])

    def _image_exists(self) -> bool:
        """Check if the Docker image already exists."""
        result = subprocess.run(
            ["docker", "images", "-q", self.image_name], capture_output=True, text=True
        )
        return bool(result.stdout.strip())

    def run_command(self, command: Optional[List[str]] = None) -> None:
        """
        Run a command in a Docker container with the specified configuration.

        Args:
            command: Command to run in the container (default: based on config)
        """
        # Get values from config
        port = self.config.get("port")
        force_rebuild = self.config.get("force_rebuild", False)

        # Use command from parameters or config
        if command is None:
            agent_script = self.config.get("agent_script")
            command = ["python", agent_script]

        # Build the image if it doesn't exist or if forced
        if not self._image_exists() or force_rebuild:
            self.rebuild_image()

        # Base command
        cmd = [
            "docker",
            "run",
            "-it",  # Interactive with TTY
            "--rm",  # Remove when done
            "-v",
            f"{self.mount_path}:{self.working_dir}:ro",  # Mount directory as read-only
            "-v",
            f"{self.host_data_path}:{self.data_dir}",  # Mount data directory as read-write
        ]

        # Add port mapping if specified
        if port:
            cmd.extend(["-p", f"{port}:{port}"])
            print(f"Port mapping: {port} -> {port}")

        # Add working directory
        cmd.extend(["-w", self.working_dir])

        # Add image name
        cmd.append(self.image_name)

        # Add the command
        cmd.extend(command)

        # Run it
        print(f"Running: {' '.join(cmd)}")
        print(f"Mounting: {self.mount_path} -> {self.working_dir} (read-only)")
        print(f"Mounting: {self.host_data_path} -> {self.data_dir} (read-write)")
        print("Press Ctrl+C to stop the container")

        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal. Container will be stopped.")
