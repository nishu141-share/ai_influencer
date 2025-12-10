"""
AI Influencer Automation - Main Entry Point
Run this file to generate daily content
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.automation import AIInfluencerAutomation


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Influencer Automation System'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/influencer_config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--video-type',
        type=str,
        choices=['long_form', 'short_form', 'both'],
        default='both',
        help='Type of video to generate'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (no publishing)'
    )
    
    args = parser.parse_args()
    
    # Check for required API keys
    required_keys = ['GEMINI_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print("❌ Missing required API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease set them in your .env file or environment variables.")
        print("\nExample .env file:")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        print("PEXELS_API_KEY=your_pexels_api_key_here (optional)")
        sys.exit(1)
    
    # Initialize automation
    print("\n" + "="*70)
    print(" "*20 + "AI INFLUENCER AUTOMATION")
    print("="*70 + "\n")
    
    automation = AIInfluencerAutomation(config_path=args.config)
    
    # Generate content based on type
    if args.video_type == 'both':
        print("\n📹 Generating both long-form and short-form content...")
        automation.run_daily_automation()
    elif args.video_type == 'long_form':
        print("\n📹 Generating long-form content...")
        automation.generate_daily_content(video_type='long_form')
    elif args.video_type == 'short_form':
        print("\n📹 Generating short-form content...")
        automation.generate_daily_content(video_type='short_form')
    
    print("\n" + "="*70)
    print("✅ Automation complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
