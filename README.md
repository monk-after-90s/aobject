# aobject
#### In asyncio, function is not welcome because it is not compatible with coroutine. However when we instantiate a class, we use the function __init__ indeed. In some case, annoying problems arise,like:

```Python
import aiomysql
class C:
    def __init__(self):
        self.mysql_pool=await aiomysql.create_pool(host='127.0.0.1', 
                                                   port=3306,
                                                   user='root',
                                                   password=123456,
                                                   db='database',
                                                   charset='utf8')
```

#### So you can get nothing but error. In a function you can not get anything returned buy a coroutine. This is what the object is built for originally. Hope it will grow up.
