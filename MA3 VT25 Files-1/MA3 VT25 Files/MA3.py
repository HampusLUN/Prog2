""" MA3.py

Student: Hampus Lundgren
Mail: hampus.lundgren.4847@student.uu.se
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import functools
from volume_parallel import sphere_volume_parallel1, sphere_volume_parallel2


def approximate_pi(n): # Ex1
    #n is the number of points
    print('Number of points: ', n) # Print the number of points
    coordinate_list = []
    outside_points = []
    n_c = 0
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if (x**2 + y**2) <= 1:
             coordinate_list.append((x,y))
             n_c+=1
        else:
             outside_points.append((x,y))
    pi = 4*n_c/n
    print(f"Estimated value for Pi:  {pi}")
        # Separera koordinater för plotting
    inside_x, inside_y = zip(*coordinate_list)
    outside_x, outside_y = zip(*outside_points)

    # Rita punkterna
    plt.figure(figsize=(6,6))
    plt.scatter(inside_x, inside_y, color='red', s=1, label='Inside circle')
    plt.scatter(outside_x, outside_y, color='blue', s=1, label='Outside circle')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Monte Carlo Approximation of Pi')
    plt.legend()
    plt.show()
    return pi

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    points = [(random.uniform(-1,1) for _ in range(d)) for _ in range(n)] # Generates n tuples of size d
    distances = list(map(lambda point: sum(map(lambda x: x**2, point)), points)) # Calculate distances to points
    points_inside = list(filter(lambda x: x<=1, distances)) # Use filter to extract the points inside the hypersphere
    n_i = len(points_inside)
    v = n_i / n * 2**d
    return v

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    return m.pi**(d/2)/m.gamma(d/2+1)

#Ex3: parallel code - parallelize for loop
    # Multiple (np )simulations, one for each core
def sphere_volume_parallel1(n, d, np=10):
    with future.ProcessPoolExecutor() as ex:
        processes = [ex.submit(sphere_volume, n, d) for _ in range(np)] # submit(method, arg1, arg2,..)
        volumes = [p.result() for p in processes] # result() access 
    return mean(volumes)

#Ex4: parallel code - parallelize actual computations by splitting data
    # One simulation in np parts, paralellized over multiple cores
def worker_split(args): 
    n, d = args
    return sphere_volume(n, d)

def sphere_volume_parallel2(n, d, np=10):
    n_per_process = n // np
    with future.ProcessPoolExecutor() as ex:
        volumes = list(ex.map(worker_split, [(n_per_process, d)] * np)) # One worker_split performes just n // np calculations (points) instead of n
    return mean(volumes)

def main():
    #--------------Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    #--------------Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print("\n")
    print(f"EX2: Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")
    print(f"Approximated volume of {d} dimentional sphere = {sphere_volume(n, d)}")
    n = 100000
    d = 11
    vol = sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")
    print(f"Approximated volume of {d} dimentional sphere = {vol} hejhej")

    #---------------Ex3
    n = 100000 # number of points (calculations)
    d = 11 # number of dimensions of the hypersphere
    start = pc()
    volumes = []
    iterations = 10
    for _ in range (iterations):
        volumes.append(sphere_volume(n,d))
    stop = pc()
    print("\n")
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print(f"Average volume for 11-dim sphere volume: {sum(volumes)/iterations}")
    start = pc()
    vol = sphere_volume_parallel1(n,d,np=10)
    stop = pc()
    print(f"Parallel process took {stop-start} seconds")

    #----------------Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print("\n")
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    start = pc()
    sphere_volume_parallel2(n,d,np=10)
    stop = pc()
    print(f"Parallel process took {stop-start} seconds")

    
if __name__ == '__main__':
	main()