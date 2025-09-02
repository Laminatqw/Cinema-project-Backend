import os
import uuid


def upload_poster(instance, file:str)->str:
    extenstion = file.split('.')[-1]
    return os.path.join('photo_storage/poster', f"{uuid.uuid1()}.{extenstion}")




