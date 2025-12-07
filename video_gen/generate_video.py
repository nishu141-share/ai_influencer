import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate video from image and audio using SadTalker.")
    parser.add_argument("--image", required=True, help="Path to the source image")
    parser.add_argument("--audio", required=True, help="Path to the source audio")
    parser.add_argument("--output_dir", default="output", help="Directory to save the result")
    
    args = parser.parse_args()

    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    sadtalker_dir = os.path.join(project_root, "tools", "SadTalker")
    inference_script = os.path.join(sadtalker_dir, "inference.py")

    if not os.path.exists(sadtalker_dir):
        print(f"Error: SadTalker not found at {sadtalker_dir}")
        print("Please run setup_env.ps1 first.")
        sys.exit(1)

    # Check inputs
    if not os.path.exists(args.image):
        print(f"Error: Image not found: {args.image}")
        sys.exit(1)
    if not os.path.exists(args.audio):
        print(f"Error: Audio not found: {args.audio}")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Check for CUDA
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print("NVIDIA GPU detected. Using CUDA.")
        else:
            device = "cpu"
            print("No NVIDIA GPU detected. Using CPU.")
            print("WARNING: CPU generation will be SLOW. Please be patient.")
    except ImportError:
        device = "cpu"
        print("Torch not found (checking for device). Defaulting to CPU.")

    # Construct command
    # python inference.py --driven_audio <audio> --source_image <image> --result_dir <output> --still --preprocess full --device <device>
    cmd = [
        sys.executable, inference_script,
        "--driven_audio", os.path.abspath(args.audio),
        "--source_image", os.path.abspath(args.image),
        "--result_dir", os.path.abspath(args.output_dir),
        "--still", # Preprocess still image
        "--preprocess", "full",
    ]
    
    if device == "cpu":
        cmd.append("--cpu")

    print(f"Running SadTalker inference...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run in SadTalker directory to ensure relative paths work there
    try:
        subprocess.run(cmd, cwd=sadtalker_dir, check=True)
        print(f"Success! Check output in {args.output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error running SadTalker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
