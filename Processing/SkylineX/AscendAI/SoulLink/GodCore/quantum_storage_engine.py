
import zstandard as zstd
import sys

def compress(file, out):
    try:
        c = zstd.ZstdCompressor(level=22)
        with open(file, 'rb') as f, open(out, 'wb') as o:
            c.copy_stream(f, o)
        print(f"Compressed {file} -> {out}")
    except Exception as e:
        print(f"[ERROR] Compression failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python quantum_storage_engine.py <input_file> <output_file>")
    else:
        compress(sys.argv[1], sys.argv[2])
