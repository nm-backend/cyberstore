from django.conf import settings
from django.core.files.storage import FileSystemStorage


def video_storage():
    """Videos need a separate Cloudinary storage class; locally use the filesystem."""
    if settings.USE_CLOUDINARY:
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage

        return VideoMediaCloudinaryStorage()
    return FileSystemStorage()
