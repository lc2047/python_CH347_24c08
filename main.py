from i2cpy import I2C
import time

# Initialize I2C interface
i2c = I2C(id=0, driver="ch347")

# Base I2C 7-bit address for the 24C08 EEPROM
BASE_EEPROM_ADDR = 0x50

# The 24C08 is organized into 4 blocks
NUM_BLOCKS = 4

# Write and read from each block
for block_num in range(NUM_BLOCKS):
    # The device address is composed of the base address and the block select bits
    eeprom_addr = BASE_EEPROM_ADDR | block_num

    # The memory address within the block is the start of the block (0x00)
    mem_addr = 0x00

    # The data to write
    # The block number is a single integer, converted to a byte
    block_num_byte = block_num.to_bytes(1, 'big')  # 1 byte, big-endian

    # The message prefix "Block " is encoded to bytes
    message_prefix = b'Block '

    # The full data payload combines the message and the block number byte
    data_to_write = message_prefix + block_num_byte
    #data_to_write = b'Hello World!'

    # The full payload for the I2C transaction
    payload = bytes([mem_addr]) + data_to_write

    print(f"Writing to block {block_num} (I2C addr: 0x{eeprom_addr:02X})...")

    # Write the data payload to the start of the current block
    i2c.writeto(eeprom_addr, payload)

    # Wait for the EEPROM's write cycle to complete (typically 5ms)
    time.sleep(0.005)

    # Read back from the same location
    # First, write the starting memory address to set the internal pointer
    i2c.writeto(eeprom_addr, bytes([mem_addr]))

    # Read back the entire block of data.
    read_data = i2c.readfrom(eeprom_addr, len(data_to_write))

    # Separate the message and the block number from the read data
    read_message_prefix = read_data[:-1]
    read_block_num_byte = read_data[-1]

    print(f"Read from block {block_num}: {read_message_prefix.decode('utf-8')}{read_block_num_byte}")
    print("-" * 30)

print("Script finished.")
