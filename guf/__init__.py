"""guf - Git URL in Files. Extract URLs from files and directories."""

from .extractor import extract_urls, extract_from_file, extract_from_directory

__version__ = "0.1.0"
__all__ = ["extract_urls", "extract_from_file", "extract_from_directory"]
