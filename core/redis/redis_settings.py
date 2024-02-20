import redis.asyncio as redis


class RedisTools:
    """
    settings for Redis
    """
    __redis_connect = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    @classmethod
    async def get_access_token(
            cls,
            username: str,
    ):
        """
        Function to get token
        :param username: str
        :return: access_token
        """
        token = await cls.__redis_connect.get(username)
        return token

    @classmethod
    async def set_access_token(
            cls,
            username: str,
            access_token: str
    ):
        """
        Set token in redis
        :param username: str
        :param access_token: str
        :return: None
        """
        await cls.__redis_connect.set(username, access_token)

    @classmethod
    async def remove_access_token(
            cls,
            username: str
    ):
        """
        Remove token from redis
        :param username: str
        :return: None
        """
        await cls.__redis_connect.delete(username)
