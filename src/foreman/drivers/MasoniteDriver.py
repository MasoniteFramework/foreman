import os

class MasoniteDriver:

    def wsgi_path(self):
        return "wsgi.py"   
    
    def detect(self, directory):
        return os.path.exists(
            os.path.join(directory, 'bootstrap')
        )
