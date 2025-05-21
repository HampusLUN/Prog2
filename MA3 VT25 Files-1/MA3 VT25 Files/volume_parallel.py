from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from MA3 import sphere_volume

def worker(args):
    n, d = args
    return sphere_volume(n, d)

def sphere_volume_parallel1(n, d, np=10):
    with ProcessPoolExecutor() as ex:
        volumes = list(ex.map(worker, [(n, d)] * np))
    return mean(volumes)

def sphere_volume_parallel2(n, d, np=10):
    n_per_process = n // np
    with ProcessPoolExecutor() as ex:
        volumes = list(ex.map(worker, [(n_per_process, d)] * np))
    return mean(volumes)
