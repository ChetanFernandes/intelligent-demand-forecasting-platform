import yaml

def save_yaml(data, filepath):
    with open(filepath,"w") as file:
        yaml.safe_dump(data,file,sort_keys=False)