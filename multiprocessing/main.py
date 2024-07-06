import multiprocessing
import time
import os


# Функція для пошуку ключових слів у файлах
def search_keywords(files, keywords, results_queue):
    results = {}
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in results:
                            results[keyword] = []
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    results_queue.put(results)


# Основна функція для багатопроцесорного підходу
def multiprocessing_search(file_paths, keywords):
    processes = []
    num_processes = 4
    files_per_process = len(file_paths) // num_processes
    results_queue = multiprocessing.Queue()

    start_time = time.time()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (
            (i + 1) * files_per_process if i != num_processes - 1 else len(file_paths)
        )
        process_files = file_paths[start_index:end_index]
        process = multiprocessing.Process(
            target=search_keywords, args=(process_files, keywords, results_queue)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Збір результатів з усіх процесів
    results = {}
    while not results_queue.empty():
        result = results_queue.get()
        for keyword, files in result.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    end_time = time.time()
    print(f"Multiprocessing search completed in {end_time - start_time} seconds")
    return results


# Виклик функції
if __name__ == "__main__":
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]  # Ваші файли
    keywords = ["keyword1", "keyword2", "keyword3"]  # Ваші ключові слова
    results_multiprocessing = multiprocessing_search(file_paths, keywords)
    print(results_multiprocessing)
