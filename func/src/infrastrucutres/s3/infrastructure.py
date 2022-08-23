# Third party
from aioboto3 import Session
from contextlib import asynccontextmanager
from decouple import config
from etria_logger import Gladsheim


class S3Infrastructure:
    session = None

    @classmethod
    async def _get_session(cls):
        if cls.session is None:
            try:
                cls.session = Session(
                    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                    region_name=config("AWS_REGION_NAME"),
                )

            except Exception as ex:
                Gladsheim.error(error=ex, message="Error trying to get aws session")
                raise ex
        return cls.session

    @classmethod
    @asynccontextmanager
    async def get_resource(cls):
        session = await S3Infrastructure._get_session()
        try:
            async with session.resource("s3") as s3_resource:
                bucket = await s3_resource.Bucket("dtvm-visual-identity-files")
                yield bucket
        except Exception as ex:
            Gladsheim.error(error=ex, message="Error trying to get s3 resource")
            raise ex

    # @classmethod
    # @asynccontextmanager
    # async def get_bucket(cls, bucket_name: str):
    #     s3_resource = await cls.get_resource()
    #     try:
    #         bucket = await s3_resource.Bucket(bucket_name)
    #         yield bucket
    #     except Exception as ex:
    #         Gladsheim.error(error=ex, message="Error trying to get bucket")
    #         raise ex
