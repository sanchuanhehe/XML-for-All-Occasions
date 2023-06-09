from xml.sax.handler import ContentHandler#ContentHandler 类是 SAX 应用程序的主要接口，它负责处理 SAX 事件。ContentHandler 接口必须由应用程序实现。
from xml.sax import parse#parse() 函数解析一个 XML 文档，第一个参数是文件名或类文件对象，第二个参数是 ContentHandler 类的实例。
import os#os 模块提供了非常丰富的方法用来处理文件和目录


# 创建一个分配器类,分配器类继承自ContentHandler类，用于分配方法调用，根据节点名调用相应的方法，如果没有相应的方法则调用默认的方法，如果没有默认的方法则不做任何处理，这样就可以只实现需要的方法，而不用实现所有的方法
class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        # 生成一个方法名
        mname = prefix + name.capitalize()
        # 生成一个默认的方法名
        dname = 'default' + prefix.capitalize()
        # 尝试获取方法
        method = getattr(self, mname, None)
        # 如果方法可调用
        if callable(method):#callable() 函数用于检查一个对象是否是可调用的。如果返回 True，object 仍然可能调用失败；但如果返回 False，调用对象 object 绝对不会成功。
            args = ()# 设置参数为空
        else:
            # 尝试获取默认方法
            method = getattr(self, dname, None)
            # 设置参数为节点名
            args = name,
        # 如果是起始节点
        if prefix == 'start':
            args += attrs,
        # 如果方法可调用
        if callable(method):
            # 调用方法
            method(*args)#*args 表示将参数打包成tuple给函数体调用

    # 定义起始节点方法
    def startElement(self, name, attrs):#attrs是一个字典,包含节点的属性,键是属性名,值是属性值
        # 分配方法调用
        self.dispatch('start', name, attrs)

    # 定义结束节点方法
    def endElement(self, name):
        # 分配方法调用
        self.dispatch('end', name)


# 创建一个网站构建类，继承自分配器和内容处理器
class WebsiteConstructor(Dispatcher, ContentHandler):

    # 是否直接输出节点及其内容
    passthrough = False

    #os.makedirs() 方法用于递归创建目录。像 mkdir(), 但创建的所有intermediate-level文件夹需要包含子文件夹。

    # 初始化方法，传入目录路径
    def __init__(self, directory):
        # 设置目录列表
        self.directory = [directory]#directory是一个列表,包含了目录的路径
        # 确保目录存在
        self.ensureDirectory()

    # 确保目录存在的方法
    def ensureDirectory(self):
        # 拼接出目录路径
        path = os.path.join(*self.directory)
        # 目录不存在则创建
        os.makedirs(path, exist_ok=True)

    # 处理普通文本节点的方法
    def characters(self, chars):
        # 如果要直接输出节点
        if self.passthrough:
            # 写入内容
            self.out.write(chars)

    # 如果没有相应的方法，使用默认的起始节点方法
    def defaultStart(self, name, attrs):
        # 如果要直接输出节点
        if self.passthrough:
            # 输出起始标签
            self.out.write('<' + name)
            # 输出属性
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            # 输出结束标签
            self.out.write('>')

    # 如果没有相应的方法，使用默认的结束节点方法
    def defaultEnd(self, name):
        # 如果要直接输出节点
        if self.passthrough:
            # 输出结束标签
            self.out.write('</{}>'.format(name))

    # 处理目录起始节点的方法
    def startDirectory(self, attrs):
        # 在目录列表中添加目录名
        self.directory.append(attrs['name'])
        # 确保目录存在
        self.ensureDirectory()

    # 处理目录结束节点的方法
    def endDirectory(self):
        # 在目录列表中删除最后一个目录
        self.directory.pop()

    # 处理页面起始节点的方法
    def startPage(self, attrs):
        # 生成文件名
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        # 打开文件
        self.out = open(filename, 'w')
        # 写入头部信息
        self.writeHeader(attrs['title'])
        # 开启直接输出
        self.passthrough = True

    # 处理页面结束节点的方法
    def endPage(self):
        # 关闭直接输出
        self.passthrough = False
        # 写入尾部信息
        self.writeFooter()
        # 关闭文件
        self.out.close()

    # 写入头部信息的方法，传入页面标题
    def writeHeader(self, title):
        self.out.write('<html>\n <head>\n <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n <body>\n')

    # 写入尾部信息的方法
    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')


# 解析并构建网站
parse('website.xml', WebsiteConstructor('output'))


# 以下是课本上的代码
"""
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os


class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if callable(method):
            args = ()
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == 'start':
            args += attrs,
        if callable(method):
            method(*args)

    def startElement(self, name, attrs):
        self.dispatch('start', name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class WebsiteConstructor(Dispatcher, ContentHandler):

    passthrough = False

    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        os.makedirs(path, exist_ok=True)

    def characters(self, chars):
        if self.passthrough:
            self.out.write(chars)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            self.out.write('>')

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write('</{}>'.format(name))

    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs['title'])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n <head>\n <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n <body>\n')

    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')


parse('website.xml', WebsiteConstructor('public_html'))
"""
