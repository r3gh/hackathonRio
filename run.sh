#!/bin/sh
python3 -m nltk.downloader rslp
echo "Running OTT and OFR Crawler";
cd ott-crawler
python3 run.py &
echo "Tweet Crawler";
cd ..
cd twitterAPI
python3 crawlerTwitter.py &
echo "Build Databaser"
python3 build_locality_dataset.py &
echo "Tranform Tweet";
python3 transformTwitter.py &
echo "Tweet Stream";
python3 streamTwitter.py &
