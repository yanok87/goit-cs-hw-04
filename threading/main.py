import threading
import time
import os

import os

# Створення тестових файлів з випадковим вмістом
file_names = ["file1.txt", "file2.txt", "file3.txt"]
for file_name in file_names:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(
            f"This is a test file for {file_name}. It contains some test keywords such as keyword1, keyword2, and keyword3."
        )


# Функція для пошуку ключових слів у файлах
def search_keywords(files, keywords, results, lock):
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        with lock:
                            if keyword not in results:
                                results[keyword] = []
                            results[keyword].append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")


# Основна функція для багатопотокового підходу
def multithreading_search(file_paths, keywords):
    threads = []
    num_threads = 4
    files_per_thread = len(file_paths) // num_threads
    results = {}
    lock = threading.Lock()

    start_time = time.time()

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (
            (i + 1) * files_per_thread if i != num_threads - 1 else len(file_paths)
        )
        thread_files = file_paths[start_index:end_index]
        thread = threading.Thread(
            target=search_keywords, args=(thread_files, keywords, results, lock)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Multithreading search completed in {end_time - start_time} seconds")
    return results


# Виклик функції
if __name__ == "__main__":
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]  # Ваші файли
    keywords = ["keyword1", "keyword2", "keyword3"]  # Ваші ключові слова
    results_threading = multithreading_search(file_paths, keywords)
    print(results_threading)
