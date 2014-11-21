import boto
import boto.rds
import boto.ec2.cloudwatch
from django.conf import settings

def boto_init_s3(bucket_name):
    """
    Init boto s3 with credentials
    :param bucket_name: name of the bucket wanted
    :return: return the bucket obtain
    """
    c = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket_name)

    return b


def boto_init_ec2():
    return boto.ec2.cloudwatch.connect_to_region("us-east-1",
                                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def boto_init_rds():
    return boto.rds.connect_to_region("us-east-1",
                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)