# Copyright 2017 Ben Gidley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess
from argparse import ArgumentParser

import av

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

parser = ArgumentParser()
parser.add_argument("input", help="Input video file - typically a TS")
parser.add_argument("--dry-run", dest="dry", action='store_true', default=False)
args = parser.parse_args()
logging.debug("Arguments: %s", args)

inputContainer = av.open(args.input)

commandLine = "ffmpeg -i \"{}\"".format(args.input)

assert len(inputContainer.streams.video) == 1
videoStream = inputContainer.streams[0]
if videoStream.name == 'h264':
    # Convert without Video transcode
    commandLine += " -map 0:v -c:v copy"
else:
    # Video Transcode
    commandLine += " -map 0:v -c:v -c:v libx264 -crf 20 -profile:v high -level 4.1"

for i, audioStream in enumerate(inputContainer.streams.audio):
    logging.debug(audioStream)
    if audioStream.language == 'eng' and audioStream.layout.name == "stereo":
        commandLine += ' -map 0:{}:a -c:a ac3 -strict -2 -q:a 128k -ar 48000'.format(audioStream.index)

commandLine += ' -movflags faststart -analyzeduration 6000 -probesize 1000000 -sn -y "{}"'.format(
    args.input.replace(".ts", ".mp4"))

if args.dry:
    print(commandLine)
else:
    print("Executing")
    subprocess.run(args=[commandLine], shell=True)