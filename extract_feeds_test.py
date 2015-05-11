#!/usr/bin/env python3

import unittest
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extract_feeds import *

class TestFeeds(unittest.TestCase):
    def test_empty_initialization(self):
        feeds = Feeds()
        self.assertEqual(feeds.get_rss_list(), [])
        self.assertEqual(feeds.get_atom_list(), [])

    def test_add_rss_items(self):
        feeds = Feeds()
        feeds.add_rss('a')
        feeds.add_rss('b')
        self.assertEqual(feeds.get_rss_list(), ['a', 'b'])

    def test_add_atom_items(self):
        feeds = Feeds()
        feeds.add_atom('c')
        feeds.add_atom('d')
        feeds.add_atom('e')
        self.assertEqual(feeds.get_atom_list(), ['c', 'd', 'e'])
    
    def test_json(self):
        feeds = Feeds()
        feeds.add_rss('a')
        self.assertEqual(json.loads(feeds.get_json()), {'rss': ['a'], 'atom': []})

    def test_json_compact(self):
        feeds = Feeds()
        self.assertFalse(' ' in feeds.get_json())

    def test_json_beautify(self):
        feeds = Feeds()
        self.assertEqual(json.loads(feeds.get_json(indent=True)), {'rss': [], 'atom': []})
        self.assertTrue('    ' in feeds.get_json(indent=True))
        self.assertFalse('     ' in feeds.get_json(indent=True))
        feeds.add_atom('a')
        self.assertEqual(json.loads(feeds.get_json(indent=True)), {'rss': [], 'atom': ['a']})
        self.assertTrue('        ' in feeds.get_json(indent=True))
        self.assertFalse('         ' in feeds.get_json(indent=True))
    
    def test_unicode(self):
        feeds = Feeds()
        feeds.add_rss('ű')
        self.assertTrue(r'"\u0171"' in feeds.get_json())

class TestFileReader(unittest.TestCase):
    def test_different_encodings(self):
        dirname = os.path.dirname(os.path.abspath(__file__)) + '/test_files/file_reader'
        for filename in os.listdir(dirname):
            contents = get_file_contents(dirname + '/' + filename)
            self.assertTrue('<link type="rss">' in contents)


class TestExtractor(unittest.TestCase):
    def test_empty_html(self):
        feeds = parse_feeds('<html><head><title></title></head><body></body></html>')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':[], 'atom': []})
    
    def test_simple_rss_atom_link(self):
        feeds = parse_feeds('''
            <html><head><title></title>
                <link href="a" type="application/atom+xml">
                <link href="r" type="application/rss+xml">
            </head><body>
            </body></html>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':['r'], 'atom': ['a']})

    def test_simple_rss_atom_anchor(self):
        feeds = parse_feeds('''
            <html><head><title></title>
            </head><body>
                <a href="r" type="application/rss+xml"></a>
                <a href="a" type="application/atom+xml"></a>
            </body></html>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':['r'], 'atom': ['a']})

    def test_anchor_with_others(self):
        feeds = parse_feeds('''
            <html><head><title></title>
            </head><body>
                <a href="r" 
                   type="application/rss+xml"
                   target="_blank"></a>
            </body></html>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':['r'], 'atom': []})

    def test_uppercased(self):
        feeds = parse_feeds('''
            <HTML><HEAD><TITLE></TITLE>
                <LINK HREF="r" TYPE="APPLICATION/RSS+XML">
            </HEAD><BODY>
                <A HREF="a" TYPE="APPLICATION/ATOM+XML"></A>
            </BODY></HTML>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':['r'], 'atom': ['a']})

    def test_commented(self):
        feeds = parse_feeds('''
            <html><head><title></title>
                <!-- <link href="a" type="application/atom+xml"> -->
                <link href="r" type="application/rss+xml">
            </head><body>
                <a href="r" type="application/rss+xml"></a>
                <!-- <a href="a" type="application/atom+xml"></a> -->
            </body></html>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':['r', 'r'], 'atom': []})

    def test_script(self):
        feeds = parse_feeds('''
            <html><head><title></title>
                <script type="text/javascript">
                    var link1 = '<link href="a" type="application/atom+xml">';
                </script>
            </head><body>
                <script type="text/javascript">
                    var link2 = '<a href="r" type="application/rss+xml"></a>';
                </script>
            </body></html>
        ''')
        self.assertEqual(json.loads(feeds.get_json()),{'rss':[], 'atom': []})

class TestMain(unittest.TestCase):
    def test_main(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/test_files/')
        try:
            os.unlink('output.json')
        except:
            pass

        main([])
        
        with open('input.json') as f:
            expected = f.read()
        with open('output.json') as f:
            result = f.read()

        os.unlink('output.json')

        self.assertEqual(json.loads(result), json.loads(expected))

if __name__ == "__main__":
    unittest.main()
