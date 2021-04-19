import argparse

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
                        help="URL from domain to scrape")
    parser.add_argument("-l", "--login", 
                        help="specify you require logging into website to scrape",
                        action="store_true")
    return parser.parse_args()