from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHALLENGE = ROOT / "challenge"


def main():
    required_paths = [
        CHALLENGE / "app.py",
        CHALLENGE / "config.py",
        CHALLENGE / "requirements.txt",
        CHALLENGE / "seed.py",
        CHALLENGE / "Dockerfile",
        CHALLENGE / "docker-compose.yml",
        CHALLENGE / "models",
        CHALLENGE / "routes",
        CHALLENGE / "templates",
        CHALLENGE / "static",
        CHALLENGE / "uploads",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required challenge paths: {', '.join(missing)}")
    print("Challenge structure check passed.")


if __name__ == "__main__":
    main()
