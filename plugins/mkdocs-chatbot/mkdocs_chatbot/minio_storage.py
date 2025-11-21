"""
MinIO Storage Manager for ChatBot Plugin

Manages document storage in MinIO (S3-compatible object storage).
Used for storing source documents, generated documentation, and attachments.
"""

import logging
from typing import Optional, List, Dict, Any, BinaryIO
from pathlib import Path
import io

logger = logging.getLogger('mkdocs.plugins.chatbot.minio')


class MinioStorageManager:
    """
    Manages document storage in MinIO.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize MinIO storage manager.

        Args:
            config: MinIO configuration dictionary
                - endpoint: MinIO server endpoint (e.g., 'localhost:9000')
                - access_key: Access key
                - secret_key: Secret key
                - bucket_name: Bucket name for documentation
                - secure: Use HTTPS (default: True)
                - region: Optional region
        """
        self.config = config
        self.endpoint = config.get('endpoint', 'localhost:9000')
        self.access_key = config.get('access_key')
        self.secret_key = config.get('secret_key')
        self.bucket_name = config.get('bucket_name', 'mkdocs-documentation')
        self.secure = config.get('secure', True)
        self.region = config.get('region', 'us-east-1')

        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize MinIO client."""
        try:
            from minio import Minio

            if not self.access_key or not self.secret_key:
                logger.error("MinIO access_key and secret_key are required")
                return

            self.client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
                region=self.region
            )

            # Create bucket if it doesn't exist
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
            else:
                logger.info(f"MinIO bucket '{self.bucket_name}' already exists")

            logger.info(f"MinIO storage initialized: {self.endpoint}/{self.bucket_name}")

        except ImportError:
            logger.error("MinIO client not installed. Install with: pip install minio")
            self.client = None
        except Exception as e:
            logger.error(f"MinIO initialization failed: {e}")
            self.client = None

    def upload_file(self, file_path: str, object_name: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Upload a file to MinIO.

        Args:
            file_path: Path to file to upload
            object_name: Object name in MinIO (defaults to filename)
            metadata: Optional metadata dictionary

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return False

        try:
            if object_name is None:
                object_name = Path(file_path).name

            # Upload file
            self.client.fput_object(
                self.bucket_name,
                object_name,
                file_path,
                metadata=metadata
            )

            logger.info(f"Uploaded file to MinIO: {object_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to upload file to MinIO: {e}")
            return False

    def upload_data(self, data: bytes, object_name: str, content_type: str = 'application/octet-stream', metadata: Optional[Dict] = None) -> bool:
        """
        Upload data bytes to MinIO.

        Args:
            data: Data bytes to upload
            object_name: Object name in MinIO
            content_type: Content type
            metadata: Optional metadata dictionary

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return False

        try:
            data_stream = io.BytesIO(data)
            data_length = len(data)

            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                data_length,
                content_type=content_type,
                metadata=metadata
            )

            logger.info(f"Uploaded data to MinIO: {object_name} ({data_length} bytes)")
            return True

        except Exception as e:
            logger.error(f"Failed to upload data to MinIO: {e}")
            return False

    def download_file(self, object_name: str, file_path: str) -> bool:
        """
        Download a file from MinIO.

        Args:
            object_name: Object name in MinIO
            file_path: Local path to save file

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return False

        try:
            self.client.fget_object(
                self.bucket_name,
                object_name,
                file_path
            )

            logger.info(f"Downloaded file from MinIO: {object_name} -> {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to download file from MinIO: {e}")
            return False

    def download_data(self, object_name: str) -> Optional[bytes]:
        """
        Download data bytes from MinIO.

        Args:
            object_name: Object name in MinIO

        Returns:
            Data bytes if successful, None otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return None

        try:
            response = self.client.get_object(
                self.bucket_name,
                object_name
            )

            data = response.read()
            response.close()
            response.release_conn()

            logger.info(f"Downloaded data from MinIO: {object_name} ({len(data)} bytes)")
            return data

        except Exception as e:
            logger.error(f"Failed to download data from MinIO: {e}")
            return None

    def list_objects(self, prefix: str = '', recursive: bool = True) -> List[str]:
        """
        List objects in MinIO bucket.

        Args:
            prefix: Optional prefix to filter objects
            recursive: List recursively

        Returns:
            List of object names
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return []

        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )

            object_names = [obj.object_name for obj in objects]
            return object_names

        except Exception as e:
            logger.error(f"Failed to list objects in MinIO: {e}")
            return []

    def delete_object(self, object_name: str) -> bool:
        """
        Delete an object from MinIO.

        Args:
            object_name: Object name to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return False

        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"Deleted object from MinIO: {object_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete object from MinIO: {e}")
            return False

    def get_object_metadata(self, object_name: str) -> Optional[Dict]:
        """
        Get metadata for an object.

        Args:
            object_name: Object name

        Returns:
            Metadata dictionary if successful, None otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return None

        try:
            stat = self.client.stat_object(self.bucket_name, object_name)

            return {
                'size': stat.size,
                'last_modified': stat.last_modified,
                'etag': stat.etag,
                'content_type': stat.content_type,
                'metadata': stat.metadata
            }

        except Exception as e:
            logger.error(f"Failed to get object metadata from MinIO: {e}")
            return None

    def generate_presigned_url(self, object_name: str, expires_seconds: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary access to an object.

        Args:
            object_name: Object name
            expires_seconds: URL expiration time in seconds

        Returns:
            Presigned URL if successful, None otherwise
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return None

        try:
            from datetime import timedelta

            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(seconds=expires_seconds)
            )

            logger.info(f"Generated presigned URL for: {object_name}")
            return url

        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None

    def sync_directory(self, local_dir: str, prefix: str = '') -> int:
        """
        Sync a local directory to MinIO.

        Args:
            local_dir: Local directory path
            prefix: Optional prefix for objects in MinIO

        Returns:
            Number of files uploaded
        """
        if not self.client:
            logger.warning("MinIO client not initialized")
            return 0

        try:
            local_path = Path(local_dir)
            if not local_path.exists() or not local_path.is_dir():
                logger.error(f"Directory not found: {local_dir}")
                return 0

            count = 0
            for file_path in local_path.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path
                    relative_path = file_path.relative_to(local_path)
                    object_name = f"{prefix}{relative_path}".replace('\\', '/')

                    # Upload file
                    if self.upload_file(str(file_path), object_name):
                        count += 1

            logger.info(f"Synced {count} files from {local_dir} to MinIO")
            return count

        except Exception as e:
            logger.error(f"Failed to sync directory to MinIO: {e}")
            return 0

    def is_available(self) -> bool:
        """Check if MinIO storage is available and initialized."""
        return self.client is not None
