import struct
import zlib

def solve(data: bytes) -> str:
    png_sig = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(png_sig):
        return "Помилка: немає підпису PNG"
    
    pos = len(png_sig)
    chunks_info = []
    image_info = None
    seen_iend = False
    extra_bytes = 0

    while pos < len(data):
        if pos + 12 > len(data):
            return f"Обірваний шматок на зсуві {pos}"
        
        length = struct.unpack(">I", data[pos:pos+4])[0]
        chunk_type = data[pos+4:pos+8]
        
        chunk_total_size = 12 + length
        if pos + chunk_total_size > len(data):
            return f"Обірваний шматок на зсуві {pos}"
        
        chunk_data = data[pos+8:pos+8+length]
        crc_stored = struct.unpack(">I", data[pos+8+length:pos+12+length])[0]
        
        crc_calculated = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        crc_match = (crc_calculated == crc_stored)
        
        if not image_info:
            if chunk_type != b"IHDR" or length != 13:
                return "Помилка: перший шматок не IHDR"
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk_data[:10])
            color_map = {
                0: "відтінки сірого",
                2: "RGB",
                3: "палітра",
                4: "сірий з альфою",
                6: "RGBA"
            }
            color_str = color_map.get(color_type, f"невідомий ({color_type})")
            image_info = f"Зображення: {width}x{height}, {bit_depth} біт, {color_str}"

        chunks_info.append((chunk_type.decode('ascii', errors='ignore'), length, crc_match))
        
        pos += chunk_total_size
        if chunk_type == b"IEND":
            seen_iend = True
            if pos < len(data):
                extra_bytes = len(data) - pos
            break

    if not seen_iend:
        return "Немає IEND"

    lines = [image_info]
    for c_type, c_len, c_match in chunks_info:
        crc_text = "CRC збігається" if c_match else "CRC не збігається"
        lines.append(f"{c_type}: {c_len} байтів, {crc_text}")
    
    if extra_bytes > 0:
        lines.append(f"Зайвих байтів після IEND: {extra_bytes}")

    return "\n".join(lines)