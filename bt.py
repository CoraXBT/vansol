import base58
import multiprocessing
from solders.keypair import Keypair # type: ignore
import time
import sys
import os
from playsound import playsound
import threading

# Define the base-58 alphabet used in Solana addresses
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def generate_keypair():
    # Generate a new Solana keypair
    return Keypair()

def check_vanity(public_key, prefix, suffix):
    # Check if the public key matches the given prefix and/or suffix
    public_key_str = str(public_key)
    if prefix and suffix:
        return public_key_str.startswith(prefix) and public_key_str.endswith(suffix)
    elif prefix:
        return public_key_str.startswith(prefix)
    elif suffix:
        return public_key_str.endswith(suffix)
    return False

def validate_base58_string(s):
    # Validate that a string only contains characters from the base-58 alphabet
    for char in s:
        if char not in BASE58_ALPHABET:
            raise ValueError(f"Invalid character '{char}' in string. Only base-58 characters are allowed.")

def worker(prefix, suffix, queue, counter, batch_size=10):
    # Worker process to generate keypairs and check for vanity addresses
    while True:
        for _ in range(batch_size):
            keypair = generate_keypair()
            public_key = keypair.pubkey()
            if check_vanity(public_key, prefix, suffix):
                secret_key = base58.b58encode(bytes(keypair)).decode('utf-8')
                queue.put((public_key, secret_key))
                return
        with counter.get_lock():
            counter.value += batch_size

def play_notification_sound(notification_sound):
    # Play the notification sound
    playsound(notification_sound)

def find_vanity(prefix, suffix, num_processes, notification_sound, batch_size=10):
    # Find a vanity Solana address with the specified prefix and/or suffix
    validate_base58_string(prefix)
    validate_base58_string(suffix)
    
    queue = multiprocessing.Queue()
    counter = multiprocessing.Value('i', 0)  # Shared counter for wallet generation
    processes = [multiprocessing.Process(target=worker, args=(prefix, suffix, queue, counter, batch_size)) for _ in range(num_processes)]

    start_time = time.time()  # Start timer
    for p in processes:
        p.start()

    # Display the counter and timer in real-time
    while queue.empty():
        elapsed_time = time.time() - start_time
        elapsed_hours, remainder = divmod(elapsed_time, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        with counter.get_lock():
            count = counter.value
        sys.stdout.write(f'\rWallets: {count:,} | Time: {int(elapsed_hours)}:{int(elapsed_minutes):02}:{int(elapsed_seconds):02} ')
        sys.stdout.flush()
        time.sleep(1)

    public_key, secret_key = queue.get()

    for p in processes:
        p.terminate()

    # Play notification sound in a separate thread
    threading.Thread(target=play_notification_sound, args=(notification_sound,)).start()

    return public_key, secret_key

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a Solana vanity address.")
    parser.add_argument("--prefix", type=str, default="", help="The desired prefix for the vanity address.")
    parser.add_argument("--suffix", type=str, default="", help="The desired suffix for the vanity address.")
    parser.add_argument("--num_processes", type=int, default=4, help="Number of processes to use for generating addresses.")
    parser.add_argument("--notification_sound", type=str, default=r"assets\Achievement.mp3", help="Path to the MP3 file to play when a matching wallet is found.")
    args = parser.parse_args()

    try:
        public_key, secret_key = find_vanity(args.prefix, args.suffix, args.num_processes, args.notification_sound)
        print(f"\nAddress: {public_key}")
        print(f"Secret Key: {secret_key}")
    except ValueError as e:
        print(f"Error: {e}")
