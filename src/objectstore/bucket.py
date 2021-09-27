import logging
import os
import urllib.parse

from minio import Minio

from base.model import BaseModel

TEMP_DIR_DOWNLOAD = "tmp_download"

def s3encode(name_plain):
    if name_plain:
        return urllib.parse.quote_plus(name_plain)

    return ''

def s3decode(name_encoded):
    if name_encoded:
        return urllib.parse.unquote_plus(name_encoded)

    return ''



class Bucket(BaseModel):

    def __init__(self, host, port, name, access_key, secret_key):
        super().__init__()
        
        data = {}
        data["host"] = host
        data["port"] = port
        data["name"] = name
        data["access_key"] = access_key
        data["secret_key"] = secret_key

        self.from_dict(data)

    def from_dict(self, data, bucket_id=None):
        super().from_dict(data, bucket_id)

        self.bucket_name = self.value("name")

        uri = "{}:{}".format(self.value("host"), int(self.value("port")))
        self.client = Minio(uri, self.value("access_key"), self.value("secret_key"), secure=False)

        return self

    def create_if_not_exists(self):
        bucket_exists = False

        if self.client.bucket_exists(self.bucket_name):
            logging.info("bucket {} already exists. nothing done".format(self.bucket_name))
            bucket_exists = True
        else:
            self.client.make_bucket(self.bucket_name)
            logging.info("bucket {} created".format(self.bucket_name))
        
        return bucket_exists

    def objects(self, path_prefix, recursive=False):
        return self.client.list_objects(self.bucket_name, prefix=path_prefix, recursive=recursive)

    def remove(self, object_name):
        logging.info("remove {} from s3 bucket {}".format(object_name, self.bucket_name))
        return self.client.remove_object(self.bucket_name, object_name)
    
    def download(self, s3_path, object_prefix, path_download=TEMP_DIR_DOWNLOAD, recursive=False):
        file_paths = []

        if object_prefix and object_prefix.endswith('.xlsx'):
            file_name = object_prefix
            file_path = "{dir}/{file}".format(dir=path_download, file=file_name)

            file_name_encoded = s3encode(file_name)
            object_name = '{}{}'.format(s3_path, file_name_encoded)

            logging.info("download {} from s3 to {}".format(object_name, file_path))

            self.client.fget_object(self.bucket_name, object_name, file_path)
            file_paths.append(file_path)
        else:
            object_name_prefix_encoded = s3encode(object_prefix)
            object_prefix_encoded = '{}{}'.format(s3_path, object_name_prefix_encoded)

            for s3_object in self.client.list_objects(self.bucket_name, prefix=object_prefix_encoded):
                object_name = s3_object.object_name
                file_name = object_name.split('/')[-1]
                file_name_decoded = s3decode(file_name)
                file_path = "{dir}/{file}".format(dir=path_download, file=file_name_decoded)

                logging.info("download {} from s3 to {}".format(object_name, file_path))

                if not s3_object.is_dir:
                    self.client.fget_object(self.bucket_name, object_name, file_path)
                    file_paths.append(file_path)
                elif not recursive:
                    logging.warning("non-recursive download. object {} is a directory, skipping/not downloading".format(object_name))
                else:
                    next_path = "{}/{}/".format(path_prefix, object_name)
                    logging.info("recursive download for path {}".format(next_path))
                    self.download(next_path, path_download, recursive)
        
        return file_paths

    def upload(self, path_prefix, file_path):
        file_name = file_path.split('/')[-1]

        if not path_prefix.endswith('/'):
            path_prefix = "{}/".format(path_prefix)

        file_name_encoded = s3encode(file_name)
        object_path = "{dir}{file}".format(dir=path_prefix, file=file_name_encoded)
        self.client.fput_object(self.bucket_name, object_path, file_path)
        logging.info("file uploaded to s3: {}".format(object_path))


