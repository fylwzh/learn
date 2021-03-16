#常用模块常用功能
    1.  import time
        time.sleep(1)  #单位为s，但是如果想要ms的延时，可以输入小数
    2.  import os
        os.getpid()  #获取进程ID
        os.getppid()  #获取父进程ID
        os.getcwdb()    #获取python当前的运行目录
        os.system("dir")    #运行cmd指令
    3.  import random   
        random.random()  #随机生成 0~1 之间的浮点数
    4.  import sys
        #获取参数的个数
        #           0           1       2
        #python3    xxxx.py     7890    mini_frame:application
        len(sys.argv)   #以上面的参数为例，这个长度为 3 
        port = int(sys.argv[1])  # 7890
        sys.path.append("./dynamic")
        sys.path.joint("./dynamic") ？？？
    5.  #使用变量导入模块
        frame_name = "mini_frame"
        app = "application"
        frame = __import__(frame_name)
        app = getattr(frame, app_name)  # 此时app就指向了 dynamic/mini_frame模块中的application这个函数
    6.  #eval
        with open("./web_server.conf") as f:
        conf_info = eval(f.read())          # 文件中的内容如下：{"static_path":"./static","dynamic_path":"./dynamic" }
        # 此时 conf_info是一个字典里面的数据为：
        # {
        #     "static_path":"./static",
        #     "dynamic_path":"./dynamic"
        # }
    7.  hasattr(Foo, 'echo_bar')  # 判断Foo类中 是否有echo_bar这个属性

#闭包
    def line_6(k, b):
        def create_y(x):
            print(k*x+b)
        return create_y  #返回函数名称是返回函数的引用，如果想要调用函数需要加()
    line_6_1 = line_6(1, 2)
    line_6_1(2)

#装饰器
    def set_func(func):
        print("---开始进行装饰")
        def call_func(*args, **kwargs):
            print("---这是权限验证1----")
            print("---这是权限验证2----")
            # func(args, kwargs)  # 不行，相当于传递了2个参数 ：1个元组，1个字典
            return func(*args, **kwargs)  # 拆包
        return call_func

    @set_func  # 相当于 test1 = set_func(test1)
    def test1(num, *args, **kwargs):
        print("-----test1----%d" % num)
        print("-----test1----" , args)
        print("-----test1----" , kwargs)
        return "ok"

    ret = test1(100)
    print(ret)
    # 执行结果
    # ---开始进行装饰
    # ---这是权限验证1----
    # ---这是权限验证2----
    # -----test1----100
    # -----test1---- ()
    # -----test1---- {}
    # ok

#多个装饰器对同一个函数装饰
    def add_qx(func):
        print("---开始进行装饰权限1的功能---")
        def call_func(*args, **kwargs):
            print("---这是权限验证1----")
            return func(*args, **kwargs)
        return call_func
    def add_xx(func):
        print("---开始进行装饰xxx的功能---")
        def call_func(*args, **kwargs):
            print("---这是xxx的功能----")
            return func(*args, **kwargs)
        return call_func
    @add_qx
    @add_xx
    def test1():
        print("------test1------")
    test1()
    # 运行结果
    # ---开始进行装饰xxx的功能---
    # ---开始进行装饰权限1的功能---
    # ---这是权限验证1----
    # ---这是xxx的功能----
    # ------test1------

#带有参数的装饰器
    # 带有参数的装饰器装饰过程分为2步:
    # 1. 调用set_level函数，把1当做实参
    # 2. set_level返回一个装饰器的引用，即set_func
    # 3. 用返回的set_func对test1函数进行装饰（装饰过程与之前一样）
    def set_level(level_num):
        def set_func(func):
            def call_func(*args, **kwargs):
                if level_num == 1:
                    print("----权限级别1，验证----")
                elif level_num == 2:
                    print("----权限级别2，验证----")
                return func()
            return call_func
        return set_func
    @set_level(1)
    def test1():
        print("-----test1---")
        return "ok"   
    test1()
    # 运行结果
    # ----权限级别1，验证----
    # -----test1---

# print格式化输出
    str = "value1:%d, \r\nvalue2:%d"%(2,3)
    print(str)

# __pycache__中的内容是python解释器自动生成的，里面的.pyc文件也是临时的

# 列表的常用操作
    name_list = ["zhangsan", "lisi", "wangwu"]
    print(name_list.index("wangwu"))  #获取在类表中的位置
    name_list[1] = "李四"   #列表的修改
    name_list.append("王小二")  #类表的增加
    name_list.insert(1, "小美眉") #类表的插入
    temp_list = ["孙悟空", "猪二哥", "沙师弟"]
    name_list.extend(temp_list) #列表的扩展
    name_list.remove("wangwu")#列表的删除
    name_list.pop(3) #列表的弹出，不带参数弹出第一个
    name_list.clear() #列表的清空
    count = name_list.count("张三")  #统计个数
    name_list.sort(reverse=True)    #列表降序排
    name_list.reverse()  #列表反转

#元组的使用
    info_tuple = ("zhangsan", 18, 1.75, "zhangsan")
    info_tuple.index("zhangsan")
    info_tuple.count("zhangsan")

#字典的使用
    xiaoming_dict = {"name": "小明",
                    "age": 18}
    print(xiaoming_dict["name"]) #取值
    xiaoming_dict["age"] = 18 #增加 或 修改
    xiaoming_dict.pop("name") #删除                     
    xiaoming_dict.clear() #字典的清空
    temp_dict = {"height": 1.75,
                "age": 20}
    xiaoming_dict.update(temp_dict)       #字典的合并 如果被合并的字典中包含已经存在的键值对，会覆盖原有的键值对
    for key,value in xiaoming_dict.items():
        
#字符串的使用
    hello_str = "hello hello"
    print(hello_str.count("llo"))  #出现次数统计
    print(hello_str.index("llo"))  #字符串出现的位置
    hello_str.startswith("Hello")
    hello_str.endswith("world")
    hello_str.replace("world", "python")
    hello_str.split()
    result = " ".join(hello_str)     
    udp_socket.sendto(hello_str.encode("utf-8"), ("192.168.33.53", 8080))
    b"hello hello"  #用字节表示这个字符串
    r"hello .*hello" #用到的一些符号代表正则匹配符，不用使用转义字符直接按照匹配符使用

#函数传递参数的拆包
    gl_nums = (1, 2, 3)
    gl_dict = {"name": "小明", "age": 18}
    demo(*gl_nums, **gl_dict)  #如果不拆包会将（gl_nums，gl_dict）传递给gl_nums

#魔法属性
    1. __doc__     #表示类的描述信息
        class Foo:
            def func(self):
                pass
        print(Foo.__doc__)
    2. __module__ 和 __class__
        #__module__ 表示当前操作的对象在那个模块
        #__class__ 表示当前操作的对象的类是什么
        from test import Person
        obj = Person()
        print(obj.__module__)  # 输出 test 即：输出模块
        print(obj.__class__)  # 输出 test.Person 即：输出类
    3. __init__  #会在创建见对象时自动调用，
    4. __del__ #当对象在内存中被释放时，自动触发执行。
    5. __call__  # 对象名()  会调用该方法
    6. __dict__ #给类用，了输出所有的类属性方法  给对象用，则输出所有的对象属性 对象方法
    7. __str__ #print对象时会调用
    8. __getitem__、__setitem__、__delitem__
        class Foo(object):
            def __getitem__(self, key):
                print('__getitem__', key)

            def __setitem__(self, key, value):
                print('__setitem__', key, value)

            def __delitem__(self, key):
                print('__delitem__', key)
        obj = Foo()
        result = obj['k1']      # 自动触发执行 __getitem__
        obj['k2'] = 'laowang'   # 自动触发执行 __setitem__
        del obj['k1']           # 自动触发执行 __delitem__
    9. __getslice__、__setslice__、__delslice__
        class Foo(object):
            def __getslice__(self, i, j):
                print('__getslice__', i, j)
            def __setslice__(self, i, j, sequence):
                print('__setslice__', i, j)
            def __delslice__(self, i, j):
                print('__delslice__', i, j)
        obj = Foo()
        obj[-1:1]                   # 自动触发执行 __getslice__
        obj[0:1] = [11,22,33,44]    # 自动触发执行 __setslice__
        del obj[0:2]                # 自动触发执行 __delslice__
    10. __new__
    11. __enter__、__exit__ #用于实现上下文管理器

#单例   new方法先被调用，然后是init
    class MusicPlayer(object):
        instance = None
        init_flag = False
        def __new__(cls, *args, **kwargs):
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            return cls.instance

        def __init__(self):
            if MusicPlayer.init_flag:
                return
            print("初始化播放器")
            MusicPlayer.init_flag = True

    player1 = MusicPlayer()
    print(player1)
    player2 = MusicPlayer()
    print(player2) 

#类的静态方法，类方法
    class Foo(object):
        def __init__(self, name):
            self.name = name
        def ord_func(self): """ 定义实例方法，至少有一个self参数 """
            print('实例方法')
        @classmethod
        def class_func(cls): """ 定义类方法，至少有一个cls参数 """
            print('类方法')
        @staticmethod
        def static_func(): """ 定义静态方法 ，无默认参数"""
            print('静态方法') 

        f = Foo("中国")
        f.ord_func()     # 调用实例方法
        Foo.class_func()    # 调用类方法
        Foo.static_func()   # 调用静态方法

#类的多继承
    "如果一个类有多个父类，并且父类中存在相同的方法，那么子类会调用那个方法通过 print(类名.__mro__) 查看"
    print("******多继承使用super().__init__ 发生的状态******")
    class Parent(object):
        def __init__(self, name, *args, **kwargs):  # 为避免多继承报错，使用不定长参数，接受参数
            print('parent的init开始被调用')
            self.name = name
            print('parent的init结束被调用')
    class Son1(Parent):
        def __init__(self, name, age, *args, **kwargs):  # 为避免多继承报错，使用不定长参数，接受参数
            print('Son1的init开始被调用')
            self.age = age
            super().__init__(name, *args, **kwargs)  # 为避免多继承报错，使用不定长参数，接受参数
            print('Son1的init结束被调用')
    class Son2(Parent):
        def __init__(self, name, gender, *args, **kwargs):  # 为避免多继承报错，使用不定长参数，接受参数
            print('Son2的init开始被调用')
            self.gender = gender
            super().__init__(name, *args, **kwargs)  # 为避免多继承报错，使用不定长参数，接受参数
            print('Son2的init结束被调用')
    class Grandson(Son1, Son2):
        def __init__(self, name, age, gender):
            print('Grandson的init开始被调用')
            # 多继承时，相对于使用类名.__init__方法，要把每个父类全部写一遍
            # 而super只用一句话，执行了全部父类的方法，这也是为何多继承需要全部传参的一个原因
            # super(Grandson, self).__init__(name, age, gender)
            super().__init__(name, age, gender)   #参数的传入顺序是有要求的，需要与 __mro__ 一致
            print('Grandson的init结束被调用')
    print(Grandson.__mro__)
    gs = Grandson('grandson', 12, '男')
    print('姓名：', gs.name)
    print('年龄：', gs.age)
    print('性别：', gs.gender)
    print("******多继承使用super().__init__ 发生的状态******\n\n")
    运行结果：
        ******多继承使用super().__init__ 发生的状态******
        (<class '__main__.Grandson'>, <class '__main__.Son1'>, <class '__main__.Son2'>, <class '__main__.Parent'>, <class 'object'>)
        Grandson的init开始被调用
        Son1的init开始被调用
        Son2的init开始被调用
        parent的init开始被调用
        parent的init结束被调用
        Son2的init结束被调用
        Son1的init结束被调用
        Grandson的init结束被调用
        姓名： grandson
        年龄： 12
        性别： 男
        ******多继承使用super().__init__ 发生的状态******

#类多态:就是说子类可以复写父类的方法

#子类中复写 __init__后，要调用 super.__init__,不然会导致父类中的某些方法不可用。

#UDP socket  recv_data = udp_socket.recvfrom(1024) recv_data这个变量中存储的是一个元组(接收到的数据，(发送方的ip, port))

#if __name__ == "__main__":

#线程的使用  #线程互斥锁
    import threading
    t1 = threading.Thread(target=test1, args=(g_nums,))
    t1.start()
    mutex = threading.Lock()
    mutex.acquire()
    mutex.release()

#进程的使用  #进程间的数据传递Queue  #进程池
    import multiprocessing
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=download_from_web, args=(q,))  参数可省略
    p.start()

    data = [11, 22, 33, 44]
    for temp in data:
        q.put(temp)
    q.put(temp)
    data = q.get()

    po = Pool(3)  # 定义一个进程池，最大进程数3
    for i in range(0,10):
        # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        # 每次循环将会用空闲出来的子进程去调用目标
        #个人：函数 apply_async 是非阻塞的，会一次性的执行完这个for循环
        po.apply_async(worker,(i,))  
    po.close()  # 关闭进程池，关闭后po不再接收新的请求
    po.join()  # 等待po中所有子进程执行完成，必须放在close语句之后

#可迭代对象和迭代器
    #实现了 __iter__ 方法的类生成的对象为可迭代对象，在该方法中返回迭代器
    #实现了 __iter__ __next__ 方法的类生成的对象为迭代器
    class Classmate(object):
    def __init__(self):
        self.names = list()
        self.current_num = 0
    def add(self, name):
        self.names.append(name)
    def __iter__(self):
        """如果想要一个对象称为一个　可以迭代的对象，即可以使用for，那么必须实现__iter__方法"""
        return self  # 调用iter(xxobj)的时候 只要__iter__方法返回一个 迭代器即可，至于是自己 还是 别的对象都可以的, 但是要保证是一个迭代器(即实现了 __iter__  __next__方法)
    def __next__(self):
        if self.current_num < len(self.names):
            ret = self.names[self.current_num]
            self.current_num += 1
            return ret
        else:
            raise StopIteration

#生成器 yield
    # 如果一个函数中有yield语句，那么这个就不在是函数，而是一个生成器的模板
    # 如果在调用函数的时候，发现这个函数中有yield那么此时，不是调用函数，而是创建一个生成器对象
    # 生成器中的return返回值需要使用异常来捕获
    # 可以使用next()函数让生成器从断点处继续执行，即唤醒生成器（函数）、
    # 使用send也可以启动生成器，send里面的数据会 传递给第5行，当做yield a的结果，然后ret保存这个结果,,, 
    # send的结果是下一次调用yield时 yield后面的值
    # send一般不会放到第一次启动生成器，如果非要这样做 那么传递None
    def create_num(all_num):
    # a = 0
    # b = 1
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        # print(a)
        ret = yield a  # 如果一个函数中有yield语句，那么这个就不在是函数，而是一个生成器的模板
        a, b = b, a+b
        current_num += 1
    return "ok...."

    obj2 = create_num(10)
    while True:
        try:
            ret = next(obj2)
            print(ret)
        except Exception as ret:
            print(ret.value)
            break
    
#正则表达式
    """
    1. 匹配单个字符
        .	匹配任意1个字符（除了\n）
        [ ]	匹配[ ]中列举的字符
        \d	匹配数字，即0-9
        \D	匹配非数字，即不是数字
        \s	匹配空白，即 空格，tab键
        \S	匹配非空白
        \w	匹配单词字符，即a-z、A-Z、0-9、_
        \W	匹配非单词字符
    2. 匹配多个字符
        *	匹配前一个字符出现0次或者无限次，即可有可无
        +	匹配前一个字符出现1次或者无限次，即至少有1次
        ?	匹配前一个字符出现1次或者0次，即要么有1次，要么没有
        {m}	匹配前一个字符出现m次
        {m,n}	匹配前一个字符出现从m到n次
    3.匹配开头结尾
        ^	匹配字符串开头
        $	匹配字符串结尾 
    4. 匹配分组
        |	匹配左右任意一个表达式   例如:
        (ab)	将括号中字符作为一个分组
        \num	引用分组num匹配到的字符串
        (?P<name>)	分组起别名
        (?P=name)	引用别名为name分组匹配到的字符串
    """
    import re
    ret = re.match("\w{4,20}@(163|126|qq)\.com", "test@qq.com")
    print(ret.group())  # test@qq.com

    ret = re.findall(r"\d+", "python = 9999, c = 7890, c++ = 12345")
    运行结果：['9999', '7890', '12345']

#http协议实例
    浏览器---->服务器发送的请求格式如下：
	GET / HTTP/1.1
	Host: 127.0.0.1:8080
	Connection: keep-alive
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
	Upgrade-Insecure-Requests: 1
	User-Agent: Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36
	Accept-Encoding: gzip, deflate, sdch
	Accept-Language: zh-CN,zh;q=0.8

    服务器--->浏览器回送的数据格式如下:
	HTTP/1.1 200 OK
	Bdpagetype: 1
	Bdqid: 0xe87cb3f700023783
	Bduserid: 0
	Cache-Control: private
	Connection: Keep-Alive
	Content-Encoding: gzip
	Content-Type: text/html; charset=utf-8
	Cxy_all: baidu+55617f8533383cbe48d5d2b7dc84b7f0
	Date: Fri, 20 Oct 2017 00:59:55 GMT
	Expires: Fri, 20 Oct 2017 00:59:11 GMT
	Server: BWS/1.1
	Set-Cookie: BDSVRTM=0; path=/
	Set-Cookie: BD_HOME=0; path=/
	Set-Cookie: H_PS_PSSID=1463_21080_17001_20929; path=/; domain=.baidu.com
	Strict-Transport-Security: max-age=172800
	Vary: Accept-Encoding
	X-Powered-By: HPHP
	X-Ua-Compatible: IE=Edge,chrome=1
	Transfer-Encoding: chunked

	<h1>haha</h1>

#套接字socket的使用
    #哪一端先关闭那么哪一端需要等待2ML
    #使用多进程处理客户端的连接时将客户端的socket传递给新的进程，处理完后需要在子进程和主进程中都进行客户端的socket close操作
    #socket的读操作会导致进程的阻塞，如果返回结果为空，则说明对端将socket close.
    1.服务端TCP
        import socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7890端口
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server_socket.bind(("", 7890))
        tcp_server_socket.listen(128)
        new_socket, client_addr = tcp_server_socket.accept()
            request = new_socket.recv(1024)
            print(request)
            response = "HTTP/1.1 200 OK\r\n"
            response += "\r\n"
            response += "hahahhah"
            new_socket.send(response.encode("utf-8"))
            new_socket.close()
        tcp_server_socket.close()

    2.客户端TCP
        import socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(("192.168.33.11", 7890))
        send_data = input("请输入要发送的数据:")
        tcp_socket.send(send_data.encode("utf-8"))
        tcp_socket.close()
    
    3.UDP的使用
        import socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("", 7890))
        udp_socket.sendto(b"hahahah------1----", ("192.168.33.53", 8080))
        udp_socket.sendto(send_data.encode("utf-8"), ("192.168.33.53", 8080))
        recv_data = udp_socket.recvfrom(1024)
        recv_msg = recv_data[0]  # 存储接收的数据
        send_addr = recv_data[1]  # 存储发送方的地址信息
    
    4.epoll的使用
        import socket
        import re
        import select
        def service_client(new_socket, request):
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Length:%d\r\n" % len(response_body)
            response_header += "\r\n"
            response = response_header.encode("utf-8") + response_body
            new_socket.send(response)
        def main():
            tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_server_socket.bind(("", 7890))
            tcp_server_socket.listen(128)
            tcp_server_socket.setblocking(False)  # 将套接字变为非堵塞
            # 创建一个epoll对象
            epl = select.epoll()
            # 将监听套接字对应的fd注册到epoll中
            epl.register(tcp_server_socket.fileno(), select.EPOLLIN)
            fd_event_dict = dict()
        while True:
            fd_event_list = epl.poll()  # 默认会堵塞，直到 os监测到数据到来 通过事件通知方式 告诉这个程序，此时才会解堵塞
            for fd, event in fd_event_list:
                # 等待新客户端的链接
                if fd == tcp_server_socket.fileno():
                    new_socket, client_addr = tcp_server_socket.accept()
                    epl.register(new_socket.fileno(), select.EPOLLIN)
                    fd_event_dict[new_socket.fileno()] = new_socket
                elif event==select.EPOLLIN:
                    # 判断已经链接的客户端是否有数据发送过来
                    recv_data = fd_event_dict[fd].recv(1024).decode("utf-8")
                    if recv_data:
                        service_client(fd_event_dict[fd], recv_data)
                    else: #对端关闭socket
                        fd_event_dict[fd].close()
                        epl.unregister(fd)
                        del fd_event_dict[fd]
            tcp_server_socket.close()
        if __name__ == "__main__":
            main()

#with上下文管理器
    #任何实现了 __enter__() 和 __exit__() 方法的对象都可称之为上下文管理器，上下文管理器对象可以使用 with 关键字。
    # 显然，文件（file）对象也实现了上下文管理器。
    # with open("output.txt", "r") as f:
    #     f.write("Python之禅")
    class File():
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode
        def __enter__(self):
            print("entering")
            self.f = open(self.filename, self.mode)
            return self.f
        def __exit__(self, *args):
            print("will exit")
            self.f.close()
    with File('out.txt', 'w') as f:
        print("writing")
        f.write('hello, python')

#元类
    # type的第一个参数为类的名称，第二个参数为继承对象，第三个参数为属性或方法
    class A(object):
        num = 100
    def print_b(self):
        print(self.num)
    @staticmethod
    def print_static():
        print("----haha-----")
    @classmethod
    def print_class(cls):
        print(cls.num)
    B = type("B", (A,), {"print_b": print_b, "print_static": print_static, "print_class": print_class})
    b = B()
    b.print_b()
    b.print_static()
    b.print_class()
    # 结果
    # 100
    # ----haha-----
    # 100

    #__metaclass__属性
    #-*- coding:utf-8 -*-  实现将类属性bar的名称改为大写
    def upper_attr(class_name, class_parents, class_attr):  #执行这个函数时会自动将 类名称，父类，所有的类属性传递进来
        #遍历属性字典，把不是__开头的属性名字变为大写
        new_attr = {}
        for name,value in class_attr.items():
            if not name.startswith("__"):
                new_attr[name.upper()] = value
        #调用type来创建一个类
        return type(class_name, class_parents, new_attr)
    class Foo(object, metaclass=upper_attr):
        bar = 'bip'
    print(hasattr(Foo, 'bar'))
    print(hasattr(Foo, 'BAR'))
    f = Foo()
    print(f.BAR)
    #运行结果
    # False
    # True
    # bip