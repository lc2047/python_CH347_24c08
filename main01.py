from i2cpy import I2C
import time

# Initialize I2C interface
i2c = I2C(id=0, driver="ch347")

# Base I2C 7-bit address for the 24C08 EEPROM
# The block select bits (B2, B1, B0) will be added here
BASE_EEPROM_ADDR = 0x50

# The 24C08 is organized into 4 blocks of 256 bytes each
NUM_BLOCKS = 4
BLOCK_SIZE = 256

# Write and read from each block
for block_num in range(NUM_BLOCKS):
    # The device address is composed of the base address and the block select bits
    eeprom_addr = BASE_EEPROM_ADDR | block_num

    # The memory address within the block is the start of the block (0x00)
    mem_addr = 0x00

    # The multi-byte data block to write, including the block number
    # The f-string formats the message, which is then encoded to bytes
    message = f"Block {block_num} "
    data_to_write = message.encode('utf-8')

    # The full payload combines the memory address and the data to be written
    payload = bytes([mem_addr]) + data_to_write

    print(f"Writing to block {block_num} (I2C addr: 0x{eeprom_addr:02X})...")

    # Write the data block to the lowest location (0x00) of the current block
    i2c.writeto(eeprom_addr, payload)

    # Wait for the write cycle to complete (typically 5ms for a page write)
    time.sleep(0.005)

    # Read back from the same location
    # First, set the internal pointer by writing the starting address
    i2c.writeto(eeprom_addr, bytes([mem_addr]))

    # Read back the entire block of data.
    read_data = i2c.readfrom(eeprom_addr, len(data_to_write))

    # Decode the bytes back into a string for printing
    read_string = read_data.decode('utf-8')

    print(f"Read value from block {block_num}: '{read_string}'")
    print("-" * 30)

print("Script finished.")
