import yaml

def load_config(config_file = "config.yaml"):

    config_yml = open(config_file)
    config = yaml.load(config_yml)
    return config
