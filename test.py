import requests
import time
from itertools import cycle
import random
from datetime import datetime
import sys, os
import multiprocessing

stop_event = multiprocessing.Event()

def tc(f):
    start = time.time()
    ret = f()
    end = time.time()
    return (end-start, ret)


def for_duration(seconds, f):
    start = time.time()
    while time.time() - start < seconds:
        f()

HEADERS = {
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Requested-With":"XMLHttpRequest",
}

HEADERS['Cookie'] = "xxx=" + "a"*4200

def make_request(ts):
    url = "http://localhost/?eam={ts}".format(ts=time.time())
    resp = requests.get(
        url,
        headers=HEADERS,
    )
    return (time.time(), datetime.now(), url, resp.status_code)


def log(result):
    if result[0] > 20:
        print("{!r} timed out".format(result))
        stop_event.set()

    sys.stdout.write(repr(result))
    sys.stdout.write("\n")
    sys.stdout.flush()


def forever(f):
    while True:
        yield f()

gen = forever(lambda: time.time())

def step():
    log(tc(lambda: make_request(gen.next())))
    time.sleep(0.25)

def work():
    for_duration(3600, step)

def timeout(n):
    time.sleep(n)
    stop_event.set()

procs = [multiprocessing.Process(target=work)
         for i in range(40)]
procs.append(
    multiprocessing.Process(target=lambda: timeout(60))
)

for p in procs:
    p.start()

stop_event.wait()

for p in procs:
    p.terminate()
