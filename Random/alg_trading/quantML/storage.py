import boto3
from botocore.exceptions import NoCredentialsError
import os


class S3:

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client('s3', aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

    def upload_file(self, local_file, bucket, s3_file):
        try:
            self.s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def upload_directory(self, local_path, bucketname, s3_path):
        try:
            for root, dirs, files in os.walk(local_path):
                for file_name in files:
                    print(f'Uploading {os.path.join(root, file_name)} to {s3_path+file_name}')
                    self.s3.upload_file(os.path.join(root, file_name), bucketname, s3_path + file_name)
            print("Upload Successful")
            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def download_file(self, bucket, s3_file, local_file):
        print(f'Downloading {s3_file}')
        if '/' in local_file:
            if not os.path.exists(os.path.dirname(local_file)):
                os.makedirs(os.path.dirname(local_file))
        self.s3.download_file(bucket, s3_file, local_file)
        return True

    def download_directory(self, bucket, s3_path):
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=self.access_key,
                                     aws_secret_access_key=self.secret_key)
        bucket = s3_resource.Bucket(bucket)
        for obj in bucket.objects.filter(Prefix=s3_path):
            print(f'Downloading {obj.key}')
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            bucket.download_file(obj.key, obj.key)


if __name__ == "__main__":

    local_path = './../notebooks/modelfiles/tabularML/'
    bucket = 'stock-data-ml'
    s3_file = 'modelfiles/tabularML/'
    s3 = S3(os.environ['AWSACCESSKEYID'], os.environ['AWSSECRETKEY'])
    s3.download_directory(bucket, s3_file)
