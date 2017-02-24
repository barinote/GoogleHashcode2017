# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:33:42 2017

@author: Weronika
"""
import operator

class Cache:
    def __init__(self, num, x):
        self.memory = x
        self.id = num
        self.vids = []
        #self.storage = []
        #self.endpoints = []
        #self.latencies = []
        self.requests = {}
        
    def get_id(self):
        return self.id
    def get_requests(self):
        return self.requests
      
    def __str__(self):
      return

    def select_videos(self):
        sorted_requests = sorted(self.requests.items(), key=operator.itemgetter(1), reverse=True)
        con_vids = self.get_vids()
        for request in sorted_requests:
            vid = request[0]
            if (self.memory - vid_sizes[vid] > 0) and (vid not in self.vids) and (vid not in con_vids):
                self.memory -= vid_sizes[vid]
                self.vids.append(vid)
            else:
                continue
        print(self.vids)

    def sort_requests(self):
        return sorted(self.requests.items(), key=operator.itemgetter(1), reverse=True)

    def get_connected(self):
        for end in self.endpoints:
            for cache in end.caches:
                if cache not in self.connected:
                    self.connected.append(cache)

    def get_vids(self):
        vids_connected = []
        for cache in self.connected:
            for vid in cache.vids:
                if vid not in vids_connected:
                    vids_connected.append(vid)
        return vids_connected

      
class Endpoint:
    def __init__(self, num, Ld):
        self.id = num
        self.Ld = Ld
        self.caches = []
        self.latencies = []
        self.requests = {}
    def get_id(self):
        return self.id
    def get_caches(self):
        return [i.get_id() for i in self.caches]
    def get_requests(self):
        return self.requests
      
    def send_req_to_cache(self):
        for cache in self.caches:
            for movie, amount in self.requests.items():
                try:
                    cache.requests[movie] += abs(vid_popularity[movie]) + amount + vid_sizes[movie] + (self.Ld - self.latencies[self.caches.index(cache)])
                    vid_popularity[movie] -= amount/(len(endpoints))
                except KeyError:
                    cache.requests[movie] = abs(vid_popularity[movie]) + amount + vid_sizes[movie] + (self.Ld - self.latencies[self.caches.index(cache)])
                    vid_popularity[movie] -= amount / (len(endpoints))


data = open("kittens.in", 'r')
(V, E, R, C, X) = tuple([int(i) for i in data.readline().split(' ')])
vid_sizes = [int(i) for i in data.readline().split(' ')] # <- global
vid_popularity = [0] * len(vid_sizes)
used_films = []
caches = []
for i in range(C):
    caches.append(Cache(i, X))		#list of caches
endpoints = []
for i in range(E):								#list of endpoints
    (Ld, K) = tuple([int(i) for i in data.readline().split(' ')])
    new = Endpoint(i, Ld)
    for j in range(K):
        (c, Lc) = tuple([int(i) for i in data.readline().split(' ')])
        new.caches.append(caches[c])
        new.latencies.append(Lc)
    endpoints.append(new)
    
#for i in endpoints:								#updating endpoints and latencies in caches
#    c = i.get_caches()
#    for j in c:
#        caches[j].endpoints.append(i)
#        caches[j].latencies.append(i.latencies[i.caches.index(caches[j])])

for i in range(R):								#updating requests in endpoints
    (Rv, Re, Rn) = tuple([int(i) for i in data.readline().split(' ')])
    endpoints[Re].requests[Rv] = Rn
    vid_popularity[Rv] += Rn
print(vid_popularity)

for i in endpoints:         #updating request lists in caches
    i.send_req_to_cache()
for i in caches:
    i.select_videos()

def write_to_file(filename):
    with open(filename, 'w') as f:
        f.write(str(len(caches)) + '\n')
        for c in caches:
            f.write(str(c.id) + ' ' + ' '.join([str(item) for item in c.vids]) + '\n')

print(len(endpoints))
print(vid_popularity)
write_to_file('kittens22.txt')
