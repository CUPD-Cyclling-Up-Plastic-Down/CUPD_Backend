import os
from uuid import uuid4

def rename_imagefile_to_uuid(instance, filename): # 이후 재학습 필요!
    upload_to = f'upcycling/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex

    filename = f'upcycling_{instance}_{uuid}.{ext}'
    
    return os.path.join(upload_to, filename)