from concurrent.futures import as_completed, ThreadPoolExecutor
from multiprocessing import cpu_count

from domfind.core import dns

DEFAULT = "number of CPU cores"
THREAD = cpu_count()


def exec(dom, tld, raw):
    thread = THREAD
    l = -(-len(tld) // THREAD)  # ceil
    tld = [tld[i:i + l] for i in range(0, len(tld), l)]
    if len(tld) < THREAD:
        thread = len(tld)

    summ = 0
    with ThreadPoolExecutor(thread) as tp:
        fut = {tp.submit(dns.query, dom, t, raw): t for t in tld}
        for f in as_completed(fut, timeout=None):
            summ += f.result()
    return summ
