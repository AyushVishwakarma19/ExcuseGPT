import struct, zlib

W = H = 128
scale = W / 36.0
buf = bytearray(W * H * 4)

def blend(x, y, r, g, b, a=255):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 4
        alpha = a / 255.0
        buf[i]   = int(r * alpha + buf[i]   * (1 - alpha))
        buf[i+1] = int(g * alpha + buf[i+1] * (1 - alpha))
        buf[i+2] = int(b * alpha + buf[i+2] * (1 - alpha))
        buf[i+3] = max(buf[i+3], a)

def inside_round_rect(px, py, x, y, w, h, rad):
    cx = min(max(px, x + rad), x + w - rad)
    cy = min(max(py, y + rad), y + h - rad)
    return (px - cx)**2 + (py - cy)**2 <= rad**2

for y in range(H):
    for x in range(W):
        px, py = (x + 0.5) / scale, (y + 0.5) / scale
        # Outer rounded square (x=1, y=1, w=34, h=34, rx=10)
        if inside_round_rect(px, py, 1, 1, 34, 34, 10):
            if not inside_round_rect(px, py, 2.5, 2.5, 31, 31, 8.5):
                blend(x, y, 0xEA, 0xB3, 0x08)  # #EAB308 border
            else:
                blend(x, y, 0xFE, 0xF9, 0xC3)  # #FEF9C3 fill
        # Speech bubble body + tail
        in_bubble = inside_round_rect(px, py, 9, 8, 18, 16, 3.5)
        in_tail = (24 <= py <= 28) and (11.5 <= px <= 16.5 - (py - 24) * 1.25)
        if in_bubble or in_tail:
            blend(x, y, 0x18, 0x18, 0x1B)      # #18181B charcoal
        # Top yellow bar (x=13, y=12.5, w=10, h=2.2, rx=1.1)
        if inside_round_rect(px, py, 13, 12.5, 10, 2.2, 1.1):
            blend(x, y, 0xFA, 0xCC, 0x15)      # #FACC15 lemon
        # Bottom ivory bar (x=13, y=16.8, w=6.5, h=2.2, rx=1.1)
        if inside_round_rect(px, py, 13, 16.8, 6.5, 2.2, 1.1):
            blend(x, y, 0xFA, 0xF9, 0xF5)      # #FAF9F5 ivory
        # Yellow accent dot (cx=22.2, cy=17.9, r=1.3)
        if (px - 22.2)**2 + (py - 17.9)**2 <= 1.3**2:
            blend(x, y, 0xFA, 0xCC, 0x15)      # #FACC15 lemon

raw = b''.join(b'\x00' + bytes(buf[y*W*4:(y+1)*W*4]) for y in range(H))
def chunk(t, d):
    return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
open('frontend/assets/favicon.png', 'wb').write(png)
print('Updated frontend/assets/favicon.png')