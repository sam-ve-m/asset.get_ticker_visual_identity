# Jormungandr
from func.src.infrastrucutres.redis import RedisInfrastructure

# Third party
from decouple import config
from etria_logger import Gladsheim


class RedisRepository:
    redis = RedisInfrastructure.get_client()

    @classmethod
    def get(cls, key: str) -> bytes:
        ticket_custom_fields = cls.redis.get(key)
        return ticket_custom_fields

    @classmethod
    def set(cls, key, value: str):
        try:
            cls.redis.set(
                key,
                value,
                ex=int(config("REDIS_DATA_EXPIRATION_IN_SECONDS")),
            )

        except Exception as ex:
            message = f"RedisRepository::set::error to set data"
            Gladsheim.error(error=ex, message=message)
            raise ex
