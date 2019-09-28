import yaml
from pathlib import Path
import os
class Configuration:

    def get(self, key, default=''):
        return self.config().get(key, default)

    def set(self, key, value):
        config = self.config()
        print('setting value')
        if key in config and isinstance(value, list):
            print('its a list')
            # value = set(value)
            if value not in config[key]:
                config[key] += value
                config[key] = list(set(config[key]))
        elif isinstance(value, dict):
            print('its a dict')
            config.update(value)
        else:
            print('update the val')
            config.update({key: value})
        self.save(config)
    
    def remove(self, key, value):
        config = self.config()
        if key in config and isinstance(value, list):
            
            for list_value in value:
                print('looking for ', list_value, 'in', config[key])
                if list_value in value:
                    config[key].remove(list_value)
            config[key] = list(set(config[key]))
        elif isinstance(value, dict):
            """
                {'venvs', {
                    'app1': '/some/path'
                }}
            """
            print('value is', value)
            for dict_key, dict_value in value:
                print('key', dict_key, 'value', dict_value)
        else:
            pass

        self.save(config)
        
    def save(self, dictionary):
        with open(os.path.join(self.get_home_path(), '.foreman/config.yml'), 'w') as f:
            yaml.dump(dictionary, f)
    
    def config(self):
        with open(os.path.join(self.get_home_path(), '.foreman/config.yml'), 'r') as stream:
            try:
                return yaml.safe_load(stream) or {}
            except yaml.YAMLError as exc:
                print(exc)

    def get_home_path(self):
        return str(Path.home())
