from concurrent.futures import ThreadPoolExecutor

threading = ThreadPoolExecutor(max_workers=5)
program_state = 0


def submit(task):
    threading.submit(task)
