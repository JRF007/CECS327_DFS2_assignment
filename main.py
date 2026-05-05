from dfs import DFS, ChordRing, ChordClient


def is_sorted_records(data: bytes) -> bool:
    lines = data.decode("utf-8").strip().split("\n")
    keys = [line.split(",")[0] for line in lines if line.strip()]
    return keys == sorted(keys)

ring = ChordRing(num_nodes=5)
chord = ChordClient(ring)
dfs = DFS(chord)
print("===== SYSTEM STARTUP =====")
ring.show_ring()
print("\n===== CREATE LOCAL INPUT FILES =====")
with open("part1.txt", "w", encoding="utf-8") as f:
    f.write("hello from part 1\n")
with open("part2.txt", "w", encoding="utf-8") as f:
    f.write("hello from part 2\n")
with open("part3.txt", "w", encoding="utf-8") as f:
    f.write("hello from part 3\n")
with open("records100.txt", "w", encoding="utf-8") as f:
    for i in range(99, -1, -1):
        f.write(f"{i:04d},name{i}\n")
print("Created part1.txt, part2.txt, part3.txt, records100.txt")
print("\n===== DFS DEMO: TOUCH + 3 APPENDS + READ =====")
dfs.touch("combined.txt")
dfs.append("combined.txt", "part1.txt")
dfs.append("combined.txt", "part2.txt")
dfs.append("combined.txt", "part3.txt")
print("Files:", dfs.ls())
print("combined.txt metadata:", dfs.stat("combined.txt"))
print("combined.txt contents:")
print(dfs.read("combined.txt").decode("utf-8"))
print("\n===== SORTING DEMO: 100 RECORDS =====")
dfs.touch("records100.txt")
dfs.append("records100.txt", "records100.txt")
dfs.distributed_sort_file("records100.txt", "sorted_records100.txt")
sorted_data = dfs.read("sorted_records100.txt")
print("Sorted correctly:", is_sorted_records(sorted_data))
print("First 5 sorted records:")
print("\n".join(sorted_data.decode("utf-8").strip().split("\n")[:5]))
print("\n===== PAXOS LOG SUMMARY =====")
for i, node in enumerate(ring.nodes):
    print(f"Node {i} log entries: {len(node.paxos_log)}")
    for msg_type, seq, op in node.paxos_log[:6]:
        print(f"  {msg_type}, seq={seq}, key={op[0]}")
    if len(node.paxos_log) > 6:
        print("  ...")

print("\n===== FAILURE DEMO: FOLLOWER CRASH =====")
ring.nodes[1].alive = False
print(f"Simulated crash: node 1 is now down")
with open("part4.txt", "w", encoding="utf-8") as f:
    f.write("append after follower crash\n")
dfs.append("combined.txt", "part4.txt")
print("Append after crash completed.")
print("combined.txt after crash append:")
print(dfs.read("combined.txt").decode("utf-8"))
print("\n===== FINAL CLEANUP DEMO =====")
dfs.delete_file("combined.txt")
dfs.delete_file("records100.txt")
dfs.delete_file("sorted_records100.txt")
print("Final files:", dfs.ls())