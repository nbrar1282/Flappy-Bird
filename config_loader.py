# config_loader.py

import toml

def load_config(file_path):
    default_config = {
        'game_settings': {
            'width': 800,
            'height': 600,
            'bg_color': [213, 111, 190],
            'max_vspeed': 5,
            'jump_boost': 10,
            'pipe_color': [210, 210, 220],
            'speed' :20
        }
    }
    
    try:
        with open(file_path, 'r') as config_file:
            return toml.load(config_file)
    except FileNotFoundError:
        # If there's no config file, return the default configuration
        return default_config

# Try to load the config from 'config.toml' or fallback to defaults
config = load_config("config.toml")
