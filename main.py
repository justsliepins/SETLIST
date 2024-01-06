import json
import os
from datetime import datetime

from setlist_manager import SetlistManager
from setlist_manager_ui import SetlistManagerUI
sm = SetlistManager()
sm_ui = SetlistManagerUI(sm)
sm_ui.run()


