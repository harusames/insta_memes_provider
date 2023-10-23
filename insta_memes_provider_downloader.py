import os.path
import subprocess
import sys
from datetime import datetime

from lib import read_file

logs_file_path = f'/mnt/e/logs/{os.path.splitext(os.path.basename(__file__))[0]}/{datetime.now().isoformat().replace(":", "-")}'
logs_file = open(logs_file_path, 'w')
links = read_file(sys.argv[1]).split("\n")
errors_found = False

for index, link in enumerate(links):
    print(f'Downloading {index + 1}/{len(links)}: {link}')
    # TODO: finish this
    try:
        # yt-dlp -P "${2:-/tmp}" "$1"
        command = ["yt-dlp", "-P", "/mnt/e/media/reels/de-trimis/", link]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Get the exit code
        exit_code = process.returncode

        # You can handle the output (stdout, stderr) as needed
        # print("Output:", stdout.decode("utf-8"))
        print("Error:", stderr.decode("utf-8"))

        return exit_code
    except Exception as e:
        print("Error:", e)
        return 1  # Return a non-zero exit code to indicate an error


logs_file.close()

if errors_found:
    print(f'Errors found!!! Logs saved to {logs_file_path}')
else:
    print("Overall success!")