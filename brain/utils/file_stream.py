import gzip

_file_streams = {
    'native': open,
    'gzip': gzip.open
}
