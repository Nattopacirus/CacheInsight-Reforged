import csv
import random

def generate_addresses(filename, num_addresses):
    print(f"Generating {num_addresses} addresses into {filename}...")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Address"])
        for _ in range(num_addresses):
            # Generate a 32-bit hex address (8 hex digits)
            addr = f"0x{random.randint(0, 0xFFFFFFFF):08X}"
            writer.writerow([addr])
    print("Done!")

if __name__ == "__main__":
    generate_addresses("1M_addresses.csv", 1000000)
