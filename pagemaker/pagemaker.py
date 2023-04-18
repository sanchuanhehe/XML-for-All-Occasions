from xml.sax.handler import ContentHandler
from xml.sax import parse


class PageMaker(ContentHandler):

    # 开始解析时，默认不写原始XML文件内容
    passthrough = False

    def startElement(self, name, attrs):
        if name == 'page':  # 如果解析到一个page节点
            self.passthrough = True  # 开始写入 HTML 内容
            self.out = open(attrs['name'] + '.html', 'w')  # 打开文件句柄，写入新页面
            self.out.write('<html><head>\n')  # 新页面头部标签
            self.out.write(
                '<title>{}</title>\n'.format(attrs['title']))  # 新页面标题
            self.out.write('</head><body>\n')
        elif self.passthrough:  # 如果已经开始写入新页面，则正常写入标签
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            self.out.write('>')

    def endElement(self, name):
        if name == 'page':  # 如果一个页面构造完成
            self.passthrough = False  # 停止写入HTML内容
            self.out.write('\n</body></html>\n')  # 写入 HTML 结束标签
            self.out.close()  # 关闭文件句柄
        elif self.passthrough:  # 如果正在写入新页面
            self.out.write('</{}>'.format(name))  # 写入节点结束标签

    def characters(self, chars):
        if self.passthrough:  # 如果正在写入新页面，则正常写入文本内容
            self.out.write(chars)


# 解析 website.xml 文件并使用 PageMaker 类构造网页
parse('website.xml', PageMaker())
