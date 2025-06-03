import sys
import os
from app import monitor

sys.path.insert(0, '/var/www/jumon.local')
from app.bootstrap import create_app

# monitor
for file in monitor.find_all_files(os.path.dirname(os.path.abspath(__file__))):
    if (".pyd" not in file and ".pyo" not in file and ".pyc" not in file and ".py" in file) or ".html" in file:
        monitor.track(file)
monitor.track(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
monitor.start(interval=1.0)

application = create_app()
