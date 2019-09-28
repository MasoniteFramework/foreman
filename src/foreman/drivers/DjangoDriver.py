import os

class DjangoDriver:

    def wsgi_path(self, directory):
        return self.find('wsgi.py', directory)
    
    def detect(self, directory):
        return os.path.exists(
            os.path.join(directory, 'manage.py')
        )

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)