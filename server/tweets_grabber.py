from tweets.src.build_locality_dataset import BuildLocalityDataset
from tweets.src.crawler_twitter import CrawlerTwitter
from tweets.src.stream_twitter import StreamTwitterGenerator
from tweets.src.transform_twitter import TransformTweets

class TweetsGrabber:

  def __init__(self):
    CrawlerTwitter()
    BuildLocalityDataset()
    StreamTwitterGenerator()
    TransformTweets()