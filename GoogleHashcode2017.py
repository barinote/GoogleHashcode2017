import operator

class Cache:
    def __init__(self, num, x):
        self.memory = x
        self.id = num
        self.vids = []
        self.requests = {}

    def __str__(self):
        return str(self.id) + ' ' + ' '.join([str(item) for item in self.vids])

    def select_videos(self):
        self.sort_requests()

        for request in self.requests:
            vid = request[0]
            if (self.memory - vid_sizes[vid] > 0) and vid not in used_films:
                self.memory -= vid_sizes[vid]
                self.vids.append(vid)
                used_films.append(vid)
            else:
                continue

    def sort_requests(self):
        self.requests = sorted(self.requests.items(), key=operator.itemgetter(1), reverse=True)
        return self.requests

      
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
                    cache.requests[movie] += abs(vid_popularity[movie]) + amount + vid_sizes[movie] \
                                            + 10*(self.Ld - self.latencies[self.caches.index(cache)])
                    vid_popularity[movie] -= 2*amount/(len(endpoints))
                except KeyError:
                    cache.requests[movie] = abs(vid_popularity[movie]) + amount + vid_sizes[movie] \
                                            + 10*(self.Ld - self.latencies[self.caches.index(cache)])
                    vid_popularity[movie] -= 2*amount / (len(endpoints))


def write_result_to_file(filename):
    with open(filename, 'w') as f:
        f.write(str(len(caches)) + '\n')
        for c in caches:
            f.write(str(c) + '\n')


def main(input_filename, output_filename):
    global vid_sizes, vid_popularity, used_films, endpoints, caches

    data = open(input_filename, 'r')
    (V, E, R, C, X) = tuple([int(i) for i in data.readline().split(' ')])
    vid_sizes = [int(i) for i in data.readline().split(' ')]
    vid_popularity = [0] * len(vid_sizes)
    used_films = []
    endpoints = []
    caches = []

    for i in range(C):
        caches.append(Cache(i, X))

    for i in range(E):
        (Ld, K) = tuple([int(i) for i in data.readline().split(' ')])
        new = Endpoint(i, Ld)
        for j in range(K):
            (c, Lc) = tuple([int(i) for i in data.readline().split(' ')])
            new.caches.append(caches[c])
            new.latencies.append(Lc)
        endpoints.append(new)


    for i in range(R):
        (Rv, Re, Rn) = tuple([int(i) for i in data.readline().split(' ')])
        endpoints[Re].requests[Rv] = Rn
        vid_popularity[Rv] += Rn

    for i in endpoints:
        i.send_req_to_cache()

    for i in caches:
        i.select_videos()

    write_result_to_file(output_filename)


if __name__ == "__main__":
    main('trending_today.in', 'trending_results.txt')
