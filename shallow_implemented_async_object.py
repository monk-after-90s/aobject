'''
浅层实现的异步环境自定义类方式
缺点是占用了最后实例的__await__方法
'''
import asyncio


class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    async def __ainit__(self):
        self.b = self.b ** 2
        return await asyncio.sleep(2, self)

    def __await__(self):
        return self.__ainit__().__await__()


loop = asyncio.get_event_loop()
foo = loop.run_until_complete(Foo(2, 4))
print()
