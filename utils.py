import ctypes

def get_short_path_name(long_name):
    """
    Converte para o formato de caminho curto 8.3 do Windows.
    Essencial para evitar bugs com emojis e caracteres especiais no FFmpeg/subprocess.
    """
    output_buf_size = 0
    while True:
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        needed = ctypes.windll.kernel32.GetShortPathNameW(long_name, output_buf, output_buf_size)
        if output_buf_size >= needed:
            return output_buf.value
        output_buf_size = needed
