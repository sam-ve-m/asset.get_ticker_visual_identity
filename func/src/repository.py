# Jormungandr
from .infrastructure import S3Infrastructure

# Standards
from typing import List

# Third party
from decouple import config


class S3Repository:

    @staticmethod
    def get_ticker(ticker_path: str) -> List:
        bucket = S3Infrastructure.get_bucket(config('AWS_BUCKET_NAME'))
        result = list(bucket.objects.filter(Prefix=ticker_path))
        return result

    @staticmethod
    def generate_ticker_url(ticker_path: str ) -> str:
        s3_resource = S3Infrastructure.get_resource()
        ticker_url = s3_resource.meta.client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': config('AWS_BUCKET_NAME'),
                    'Key': ticker_path},
                ExpiresIn=3600,
            )
        return ticker_url
