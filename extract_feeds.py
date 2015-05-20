#!/usr/bin/env python3

"""RSS and Atom extractor script.

(c) Máté Farkas, May 2015

For more detailed information see the README.md file"""

import argparse
import json
import sys
from html.parser import HTMLParser

INPUT_FILENAME = 'input.html'
OUTPUT_FILENAME = 'output.json'

class Feeds:
    """A simple container class for extracted feeds.
    
    You can
    - add RSS and Atom items,
    - get these items as a list,
    - or both list in compact JSON format or with 
        optional indentation using 4 spaces.
    
    Important: there are no validation for the items.
    """

    def __init__(self):
        self.rss = []
        self.atom = []

    def get_rss_list(self):
        return self.rss

    def get_atom_list(self):
        return self.atom

    def add_atom(self, item):
        self.atom.append(item)

    def add_rss(self, item):
        self.rss.append(item)

    def get_json(self, indent=False):
        data = {
            'rss': self.rss,
            'atom': self.atom
        }
        if indent:
            return json.dumps(data, indent=4)
        else:
            return json.dumps(data, separators=(',', ':'))

def get_file_contents(filename):
    """Read a text file to a string using the right encoding.

    Or at least a valid encoding with the capability to later 
    parse the string for ascii HTML tags.
    """

    codecs = ['utf_7', 'utf_8', 'utf_32_be', 'utf_32_le',
        'utf_16_be', 'utf_16_le', 'cp1250']

    with open(filename, 'rb') as f:
        string = f.read()
        for codec_name in codecs:
            try:
                return string.decode(codec_name)
            except:
                pass
        return string.decode('cp1250', 'ignore')


def parse_feeds(text):
    """Extract the feed links from an HTML document.
    
    Parameters:
        - text: the string representation of a valid HTML 4.0.1 document
    
    Returns: a Feed object with the found feed links.
    """
    
    class MyHTMLParser(HTMLParser):
        def __init__(self, feeds):
            super().__init__()
            self.feeds = feeds

        def handle_starttag(self, tag_name, attr_list):
            if not self.is_good_tag(tag_name):
                return
            attributes = dict(attr_list)
            if not 'href' in attributes:
                return
            href = attributes['href']

            # The type attribute is case-insensitive
            # see http://www.w3.org/TR/html401/struct/links.html#adef-type-A
            type = attributes.get('type').lower()
            
            if type == 'application/atom+xml':
                self.feeds.add_atom(href)
            if type == 'application/rss+xml':
                self.feeds.add_rss(href)

        def is_good_tag(self, tag):
            return tag == 'link' or tag == 'a'

    feeds = Feeds()
    parser = MyHTMLParser(feeds)
    parser.feed(text)
    parser.close()
    return feeds

def main(argv):
    parser = argparse.ArgumentParser(
        description='Extract RSS and Atom feed links from input.html to output.json.',
        epilog='For more information see the README.md file.'
    )
    parser.add_argument('--indent', action='store_true',
                       help='indent the json file')

    options = parser.parse_args(argv)

    feeds = parse_feeds(get_file_contents(INPUT_FILENAME))
    json_text = feeds.get_json(options.indent)
    with open(OUTPUT_FILENAME, 'w') as output_file:
        output_file.write(json_text)


if __name__ == "__main__":
    main(sys.argv[1:])
