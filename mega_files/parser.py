from rest_framework.parsers import FileUploadParser  # BaseParser,


class BinaryFileParser(FileUploadParser):
    media_type = "application/octet-stream"
