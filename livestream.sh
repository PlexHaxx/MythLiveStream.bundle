#!/bin/bash
# Script to Start HLS Stream
# Should be added as "System Event" "Recording started writing"

# Server and Port where API can be reached
SERVER="127.0.0.1"
PORT="6544"

# Set the deafult parameters for the HLS Stream
# This seams to work pretty good on the iPAD over 3G

#Height 320 480 540 600 768 720 0=Auto
HEIGHT="480"
#Width 288 400 480 640 800 960 1024 1280 0=Auto
WIDTH="0"
#Video Bitrate 500000 600000 700000 800000 900000 1000000 1500000 2000000 2500000 3000000 3500000 
VBITRATE="1000000"
#AudioBitrate 32000 64000 96000 128000 192000
ABITRATE="128000"

# This finds the Recording that just started.
FILENAME=`curl -vs "http://${SERVER}:${PORT}/Dvr/GetRecordedList?StartIndex=1&Count=1&Descending=true" 2>/dev/null | xml2 | grep "FileName=" | awk -F "=" '{print $2}' | grep "mpg$"`

# This creates an HLS stream of the above recording
PLAYLIST=`curl -vs "http://${SERVER}:${PORT}/Content/AddLiveStream?FileName=${FILENAME}&StorageGroup=Default&Height=${HEIGHT}&Width=${WIDTH}&Bitrate=${VBITRATE}&AudioBitrate=${ABITRATE}" 2>/dev/null | xml2 | grep "RelativeURL=" | grep "m3u8" | awk -F "=" '{print $2}' `

echo "HLS Stream can be reached at http://${SERVER}:${PORT}${PLAYLIST}"
