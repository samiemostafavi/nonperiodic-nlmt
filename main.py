import numpy as np
import scipy
import posix_ipc
import time
import mmap

shared_memory_addr = "/5gue_frame"
FRAME_INTERVAL = 10.0

INNER_WAIT = True
OFFSET = 4.0

def truncated_gaussian(mu, sigma, lower_bound, upper_bound, size=1):
    samples = []
    while len(samples) < size:
        sample = np.random.normal(mu, sigma)
        if lower_bound <= sample <= upper_bound:
            samples.append(sample)
    return np.array(samples)

def main():

    # Create or open a shared memory object
    shm = posix_ipc.SharedMemory(
        shared_memory_addr, 
        flags=posix_ipc.O_CREAT,
        size=4
    )
    f = mmap.mmap(shm.fd, shm.size)

    # Create a counter variable
    counter = 0

    target_wall_timestamp = int(time.time_ns()) + 1e9 # set first counter 1 second from now
    target_wall_timestamp = int(np.floor(target_wall_timestamp/1.0e7)*1.0e7)

    try:
        while True:
            # Get the current wall timestamp
            current_outer_wall_timestamp = int(time.time_ns())

            # Check if the current wall timestamp equals the target wall timestamp
            if current_outer_wall_timestamp >= target_wall_timestamp:
                # inner wait offset
                if INNER_WAIT:
                    wait_time_ms = OFFSET
                    sample_ms = truncated_gaussian(0, 2, -2, 2)[0]
                    wait_time_ms += sample_ms
                    inner_target_wall_timestamp = current_outer_wall_timestamp + wait_time_ms*1e6
                    while True:
                        current_wall_timestamp = int(time.time_ns())
                        if current_wall_timestamp >= inner_target_wall_timestamp:
                            # Convert counter to bytes and write to the mmap object
                            f.seek(0)
                            f.write(counter.to_bytes(4, byteorder='little'))
                            break
                else:
                    # Convert counter to bytes and write to the mmap object
                    f.seek(0)
                    f.write(counter.to_bytes(4, byteorder='little'))

                target_wall_timestamp = current_outer_wall_timestamp + FRAME_INTERVAL*1e6

                # Increase the counter
                counter += 1

    finally:
        # Clean up the shared memory
        shm.close_fd()
        shm.unlink()


if __name__ == "__main__":
    main()




