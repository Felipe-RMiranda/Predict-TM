import base64
import imghdr
from abc import ABC

class IImgService(ABC):
    @staticmethod
    def to_base64(img_bytes):
        pass

class ImgService(IImgService):
    @staticmethod
    def to_base64(img_bytes):
        img_type = imghdr.what(None, h=img_bytes)
        mime_type = f"image/{img_type}" if img_type else "image/jpeg"
        return f"data:{mime_type};base64,{base64.b64encode(img_bytes).decode('utf-8')}"