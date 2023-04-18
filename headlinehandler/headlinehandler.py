"""
This is a test file for the xml.sax module.
the author is:  sanchuanhehe
made in:  2023-4-18
"""
from xml.sax.handler import ContentHandler
from xml.sax import parse

"""
class TestHandler(ContentHandler):
    def startElement(self, name, attrs):
        print('Start element:', name, attrs.keys())

    def endElement(self, name):
        print('End element:', name)

    def characters(self, chars):
        print('Characters:', repr(chars))
"""


class HeadlineHandler(ContentHandler):
    in_headline = False

    def __init__(self, headlines):
        super().__init__()
        self.headlines = headlines
        super().__init__()

    def startElement(self, name, attrs):
        if name == 'h1':
            self.in_headline = True

    def endElement(self, name):
        if name == 'h1':
            self.data = []
            text = ''.join(self.data)
            self.headlines.append(text)
            self.in_headline = False

    def characters(self, chars):
        if self.in_headline:
            print(chars)


#parse('website.xml', TestHandler())
headlines = []
parse('website.xml', HeadlineHandler(headlines))

#print('Headlines:\n', '\n')
for h in headlines:
    print(h)
