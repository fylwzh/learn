#常用模块常用功能
    1.  import time
        time.sleep(1)  单位为s，但是如果想要ms的延时，可以输入小数

    2.  import os
        os.getpid()  获取进程ID
        os.getppid()  获取父进程ID
    3.import random   
        random.random()  随机生成 0~1 之间的浮点数

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

#字符串的使用
    hello_str = "hello hello"
    print(hello_str.count("llo"))  #出现次数统计
    print(hello_str.index("llo"))  #字符串出现的位置
    hello_str.startswith("Hello")
    hello_str.endswith("world")
    hello_str.replace("world", "python")
    hello_str.split()
    result = " ".join(hello_str)     

#函数传递参数的拆包
    gl_nums = (1, 2, 3)
    gl_dict = {"name": "小明", "age": 18}
    demo(*gl_nums, **gl_dict)  #如果不拆包会将（gl_nums，gl_dict）传递给gl_nums

#类的常用操作
    __init__  #会在创建见对象时自动调用，
    __str__ #print对象时会调用
    __new__
    __call__  # 对象名()  会调用该方法

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

#类的多继承
    "如果一个类有多个父类，并且父类中存在相同的方法，那么子类会调用那个方法通过 print(类名.__mro__) 查看"

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
    ret = re.match("\w{4,20}@(163|126|qq)\.com", "test@qq.com")
    print(ret.group())  # test@qq.com
