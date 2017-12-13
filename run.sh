#!/bin/sh
~/Work/programs/anaconda3/bin/python -m nltk.downloader rslp
echo "Running OTT and OFR Crawler";
cd ott-crawler
~/Work/programs/anaconda3/bin/python run.py &
echo "Tweet Crawler";
cd ..
cd twitterAPI
~/Work/programs/anaconda3/bin/python crawlerTwitter.py &
echo "Build Databaser"
~/Work/programs/anaconda3/bin/python build_locality_dataset.py &
echo "Tranform Tweet";
~/Work/programs/anaconda3/bin/python transformTwitter.py &
echo "Tweet Stream";
~/Work/programs/anaconda3/bin/python streamTwitter.py &
