"""DIY Stream Deck entry point."""
import argparse
import sys


def main() -> int:
    """Run the DIY Stream Deck daemon."""
    parser = argparse.ArgumentParser(description="DIY Stream Deck")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--dry-run", action="store_true", help="Validate config without running")
    args = parser.parse_args()

    print(f"DIY Stream Deck — config: {args.config}")
    print("Not yet implemented — see roadmap in README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
