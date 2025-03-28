# Run with docker

```sh
# Build and run containers in dev profile
sudo docker compose --profile=dev up
```

## Cleanup and rebuild

Docker keeps an internal cache hard to control, therefore its usefull to sometimes clean docker build and rebuild everything from scratch. This command will only setup, 
```sh
# Cleanup and rebuild containers in dev profile
sudo docker compose --profile=dev build --no-cache
```

# Manual setup 
. pyenv/bin/activate && pip install -r requirements.txt
```sh
# Setup environment
python -m venv pyenv

# Source script to isolate python dependencies
. pyenv/bin/activate

# Install dependencies in environment
pip install -r requirements.txt
```

# Manual run

```sh
# Source environment
. pyenv/bin/activate

# Run main script
python src/main.py
```