# hook-ultralytics.py
from PyInstaller.utils.hooks import collect_data_files

# Include Ultralytics files explicitly
datas = collect_data_files('ultralytics') + [
    ('D:\\VirtualEnvironment\\SupervisorAI\\Lib\\site-packages\\ultralytics\\data', 'ultralytics\\data'),
    ('D:\\VirtualEnvironment\\SupervisorAI\\Lib\\site-packages\\ultralytics\\models', 'ultralytics\\models'),
    ('D:\\VirtualEnvironment\\SupervisorAI\\Lib\\site-packages\\ultralytics\\utils', 'ultralytics\\utils'),
]

# Add specific files if needed
# datas += [('path_to_additional_file', 'destination_folder')]

# Output the results for PyInstaller
collect_data_files('ultralytics', include_py_files=True)