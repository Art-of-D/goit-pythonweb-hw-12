import cloudinary
import cloudinary.uploader


class UploadFileService:
    """
    Service class for uploading files to Cloudinary.
    """

    def __init__(self, cloud_name, api_key, api_secret):
        """
        Initialize the service with Cloudinary configuration.

        Args:
            cloud_name (str): The Cloudinary cloud name.
            api_key (str): The Cloudinary API key.
            api_secret (str): The Cloudinary API secret.
        """
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str:
        """
        Upload a file to Cloudinary and return the URL of the uploaded image.

        Args:
            file (file): The file to upload.
            username (str): The username to use as the public ID.

        Returns:
            str: The URL of the uploaded image.
        """
        public_id = f"py_avatar/{username}"
        r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=r.get("version")
        )
        return src_url