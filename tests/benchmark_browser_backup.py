import os
import time
import shutil

# Create dummy directory structure
test_dir = "test_user_data"
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(test_dir)

# Create 500 directories with 100 files each = 50,000 files
for i in range(500):
    subdir = os.path.join(test_dir, f"dir_{i}")
    os.makedirs(subdir)
    for j in range(100):
        with open(os.path.join(subdir, f"file_{j}.txt"), "w") as f:
            f.write("dummy")

def double_walk():
    start = time.time()
    num_source_files = 0
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            num_source_files += 1

    # second walk simulation
    count = 0
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, test_dir)
            count += 1
    end = time.time()
    return end - start, num_source_files

def single_walk_list():
    start = time.time()
    files_to_zip = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            file_path = os.path.join(root, file)
            files_to_zip.append(file_path)

    num_source_files = len(files_to_zip)
    count = 0
    for file_path in files_to_zip:
        rel_path = os.path.relpath(file_path, test_dir)
        count += 1
    end = time.time()
    return end - start, num_source_files

if __name__ == "__main__":
    t1, c1 = double_walk()
    print(f"Double walk: {t1:.4f}s, files: {c1}")

    t2, c2 = single_walk_list()
    print(f"Single walk (list): {t2:.4f}s, files: {c2}")

    print(f"Improvement: {(t1-t2)/t1*100:.2f}%")

    # cleanup
    shutil.rmtree(test_dir)
