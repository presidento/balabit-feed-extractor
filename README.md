# Feed extractor

This program was created by Máté FARKAS in May 2015 as an enrollment task for BalaBit.

# The task

We are developing a blog-aggregator service. For the search engine we need a parser component
that identifies links pointing to RSS or Atom feeds.

Given an HTML document as input file `input.html` (you may assume that it is a valid HTML
4.0.1 document), we expect a JSON formatted output file `output.json` that contains all the links
(the href attributes of all `<a>` and `<link>` tags) from the input file that point to RSS or Atom
feeds, grouped by their type (i.e. into "rss" and "atom" groups).

You may assume that the system running the script has a reliable network connection and the script
has access to the network. Indenting the output is not necessary, but it has to be a valid JSON
format with the proper scheme. You don’t have to validate the internal structure of the RSS or Atom
files, it shall belong to another component of the service.

Example output:

    {
        "rss": [
            "http://example.com/rss.xml",
            "https://example.org/rss2.rss"
        ],
        "atom": [
            "http://example.net/feed",
            "http://t.co/asdfsf23fdsw234"
        ]
    }

The output must contain both the "rss" and "atom" groups, if there is no link for any of them, they
shall be empty arrays.

# Installation

Install Python 3 (tested with v3.2 in Windows, and with v3.3 in Linux) and extract the archive.

Run the tests:

    $ ./extract_feeds_test.py

If everything is OK, the script is expected to be working fine.

# Usage

Extract feeds from the `input.html` to `output.json` (in the actual directory):

    $ <path_to>/extract_feeds.py
   
The `output.json` file is in ASCII encoding with escaped unicode characters.

Same as the previous one, but with indented JSON file:

    $ <path_to>/extract_feeds.py --indent

Get the help message of the script:

    $ <path_to>/extract_feeds.py --help

# Known bugs and limitations

- There is a de-facto standard for the `type` attribute of the HTML “links pointing to RSS or Atom feeds”, but it is not strict. This script searches for the links, whose say about themselves that they are pointing to those kind of resources. But according to the [HTML 4.0.1 specification](http://www.w3.org/TR/html4/struct/links.html#adef-type-A) it is not guaranteed. The links may lie. Or the resource can be served with a different mime type. Or it is disappeared. Or there is a server error. In these cases the link actually doesn't point to an RSS or Atom resource. 
- The HTML specification allows to write relative URLs, but parsing a local file these links will not work without the knowledge of the original location. (And what's more, there can be a `base` tag among the headers which can set the base URL for the relative hrefs. It is not parsed yet.)
- Sometimes the webmaster is careless and forgets to set the `type` attribute. In this case the link appears to be an ordinal link to an another classical HTML page. For example at the [BalaBit Blog homepage](https://blogs.balabit.com) in the body part of the HTML file there is only one link to the RSS resource in the following format:
<br>`<a href="/feed/" title="Subscribe to the BalaBit Blog" rel="nofollow"><img...></a>`.<br>
Without the correct `type` attribute we are not able to detect that in reality this link points to an RSS feed. Moreover, if you clicks on [that image](https://blogs.balabit.com/feed/) you may find that in spite of that the internal structure of the received file shows that it is an RSS file, it is served as a HTML file using the `text/html` mime type. So we cannot make 100% precise detection even checking every link by requesting the header informations of the target. 
- The script tries to detect the character encoding of the input file, but it is not 100% safe: if you use a non-unicode encoding *with* URLs containing international characters, the URLs may go wrong during the parsing. But this is not a real-life example, nowadays most of the homepages uses UTF-8 encoding, especially those whose uses international URLs.     
- You may find additional RSS or Atom links using your browser: this script cannot parse elements created dynamically with JavaScript.
- This script expects that the given `input.html` is a valid HTML 4.0.1 file and the directory is writeable for `output.json`.
- This script is intended to use with normal sized files, which can be loaded in a browser. (I.e. it is not for HTML files having several 100 Mbs of size.)

# Contribution


# License

The script and the additional resources are licensed according to the GNU General Public License 2. For more information see the `LICENSE` file.
