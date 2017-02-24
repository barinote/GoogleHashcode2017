import operator

class Cache:
    def __init__(self, num, x):
        self.memory = x
        self.id = num
        self.vids = []
        self.endpoints = []
        self.latencies = []
        self.requests = {}

    def get_id(self):
        return self.id

    def __str__(self):
        return


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
                    cache.requests[movie] += amount * vid_sizes[movie] * (
                    self.Ld - self.latencies[self.caches.index(cache)])
                except KeyError:
                    cache.requests[movie] = amount * vid_sizes[movie] * (
                    self.Ld - self.latencies[self.caches.index(cache)])


data = open("me_at_the_zoo.in", 'r')
(V, E, R, C, X) = tuple([int(i) for i in data.readline().split(' ')])
vid_sizes = [int(i) for i in data.readline().split(' ')]  # <- global
caches = []
for i in range(C):
    caches.append(Cache(i, X))  # list of caches
endpoints = []
for i in range(E):  # list of endpoints
    (Ld, K) = tuple([int(i) for i in data.readline().split(' ')])
    new = Endpoint(i, Ld)
    for j in range(K):
        (c, Lc) = tuple([int(i) for i in data.readline().split(' ')])
        new.caches.append(caches[c])
        new.latencies.append(Lc)
    endpoints.append(new)

for i in endpoints:  # updating endpoints and latencies in caches
    c = i.get_caches()
    for j in c:
        caches[j].endpoints.append(i)
        caches[j].latencies.append(i.latencies[i.caches.index(caches[j])])

for i in range(R):  # updating requests in endpoints
    (Rv, Re, Rn) = tuple([int(i) for i in data.readline().split(' ')])
    endpoints[Re].requests[Rv] = Rn

for i in endpoints:  # updating request lists in caches
    i.send_req_to_cache()

for c in caches:

    sorted_requests = sorted(c.requests.items(), key=operator.itemgetter(1), reverse=True)
    films = []
    for request in sorted_requests:
        films.append(request[0])
    print(films)