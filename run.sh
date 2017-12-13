#!/bin/sh
<<<<<<< HEAD
python3 -m nltk.downloader rslp
cd server
python3 run.py &
=======
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
>>>>>>> f877ceafd560161358d01b16d3ae5bb074aac47e
