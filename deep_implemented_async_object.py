'''
深层的异步环境自定义类实现方式，兼容同步和异步环境
'''
import asyncio


class aobject(object):
    async def __anew__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__ainit__(*args, **kwargs)
        return instance

    async def __ainit__(self, *args, **kwargs):
        pass

    @classmethod
    def is_async(cls):
        '''
        判断用户重载了同步异步的哪个初始化方法
        '''
        # 同时重载__init__和__ainit__是违法的
        if '__init__' in cls.__dict__.keys() and '__ainit__' in cls.__dict__.keys():
            raise SyntaxError('It is illegal to define both __init__ and __ainit__')
        # 没有重载任何初始化函数则判断当前环境
        elif '__init__' not in cls.__dict__.keys() and '__ainit__' not in cls.__dict__.keys():
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                # 同步环境
                return False
            else:
                # 异步环境
                return True
        # 重载了__init__
        elif '__init__' in cls.__dict__.keys():
            if not asyncio.iscoroutinefunction(cls.__init__):
                return False
            else:
                raise SyntaxError('__init__ must not be a coroutine function.')
        # 重载了__ainit__
        elif '__ainit__' in cls.__dict__.keys():
            if asyncio.iscoroutinefunction(cls.__ainit__):
                return True
            else:
                raise SyntaxError('__ainit__ must be a coroutine function.')

    def __new__(cls, *args, **kwargs):
        # 判断同步环境还是异步环境
        async_env = cls.is_async()
        # 同步环境
        if not async_env:
            # 构造实例
            instance = super().__new__(cls)
            instance.__init__(*args, **kwargs)
            return instance
        # 异步环境
        else:
            # 返回异步构造协程
            return cls.__anew__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):  # 考虑使用统一的__init__来实现同步和异步
        pass


if __name__ == '__main__':
    # 测试
    async def main():
        class C(aobject):
            async def __ainit__(self):
                pass

        c = await C()
        print(c)


    asyncio.run(main())
