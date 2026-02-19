import tracemalloc

def create_heavy_list():
    print("Hi")
    return [x for x in range(100000)]

tracemalloc.start()

# Take a snapshot of current memory usage
create_heavy_list()
snapshot = tracemalloc.take_snapshot()

# Display the top memory consumers
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)


