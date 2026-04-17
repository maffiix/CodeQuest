import sys
import heapq
from collections import defaultdict, namedtuple

Edge = namedtuple("Edge", ["to", "time"])

def solve():
    all_lines = []
    try:
        while True:
            a = input()
            if a == "END_ALL":
                break
            all_lines.append(a.rstrip('\n'))
    except EOFError:
        print("INCORRECT INPUT")
        return
    
    idx = 0
    n = len(all_lines)
    
    # ---------- 1. Чтение съездов ----------
    exits = set()
    while idx < n and all_lines[idx].strip() != "END":
        token = all_lines[idx].strip()
        if not token:
            idx += 1
            continue
        
        # Проверка формата BH-01-1
        is_valid = False
        if token.startswith("BH-") and len(token) == 7:
            if (token[3].isdigit() and token[4].isdigit() and token[6].isdigit()):
                is_valid = True
        elif token.startswith("J-") and token[2:].isdigit():
            num = int(token[2:])
            if 1 <= num <= 9999:
                is_valid = True
        
        if is_valid:
            exits.add(token)
        else:
            print(f"INCORRECT INPUT: invalid exit format '{token}'")
            return
        idx += 1
    
    # Пропускаем END
    if idx < n and all_lines[idx].strip() == "END":
        idx += 1
    else:
        print("INCORRECT INPUT: expected END after exits")
        return
    
    # ---------- 2. Чтение перекрёстков ----------
    graph = defaultdict(list)
    all_nodes = set(exits)
    intersections = set()
    
    while idx < n and all_lines[idx].strip() != "END":
        line = all_lines[idx].strip()
        if not line:
            idx += 1
            continue
        parts = line.split()
        if not parts:
            idx += 1
            continue
            
        from_node = parts[0]
        # Проверка формата узла: J-число
        if not (from_node.startswith("J-") and from_node[2:].isdigit()):
            print(f"INCORRECT INPUT: invalid node format '{from_node}'")
            return
        intersections.add(from_node)
        all_nodes.add(from_node)
        
        # Каждый from_node имеет ровно 4 соединения
        if len(parts) != 5:
            print(f"INCORRECT INPUT: node {from_node} has {len(parts)-1} connections, expected 4")
            return
        
        for i in range(1, 5):
            to_part = parts[i]
            if ":" not in to_part:
                print(f"INCORRECT INPUT: invalid edge format '{to_part}' at {from_node}")
                return
            to_node, time_str = to_part.split(":")
            if not time_str.isdigit():
                print(f"INCORRECT INPUT: invalid time '{time_str}' at {from_node}->{to_node}")
                return
            time_val = int(time_str)
            
            # Проверка формата to_node
            is_valid_to = False
            if to_node.startswith("J-") and to_node[2:].isdigit():
                is_valid_to = True
            elif to_node.startswith("BH-") and len(to_node) == 7:
                if (to_node[3].isdigit() and to_node[4].isdigit() and to_node[6].isdigit()):
                    is_valid_to = True
            
            if not is_valid_to:
                print(f"INCORRECT INPUT: invalid target node format '{to_node}' at {from_node}")
                return
            
            all_nodes.add(to_node)
            if to_node.startswith("J-"):
                intersections.add(to_node)
            
            graph[from_node].append(Edge(to_node, time_val))
        
        idx += 1
    
    # Пропускаем END
    if idx < n and all_lines[idx].strip() == "END":
        idx += 1
    else:
        print("INCORRECT INPUT: expected END after intersections")
        return
    
    # Проверка: каждый съезд должен быть в соединениях у какого-то перекрёстка
    exit_nodes_in_graph = set()
    for node, edges in graph.items():
        for e in edges:
            if e.to.startswith("BH-"):
                exit_nodes_in_graph.add(e.to)
    
    for ex in exits:
        if ex not in exit_nodes_in_graph:
            print(f"INCORRECT INPUT: exit {ex} not connected to any intersection")
            return
    
    # ---------- 3. Чтение перекрытых дорог ----------
    blocked = set()
    while idx < n and all_lines[idx].strip() != "END":
        pair = all_lines[idx].strip()
        if not pair:
            idx += 1
            continue
        if ":" not in pair:
            print(f"INCORRECT INPUT: invalid blocked road format '{pair}'")
            return
        a, b = pair.split(":")
        a = a.strip()
        b = b.strip()
        # Обе стороны должны существовать
        if a not in all_nodes:
            print(f"INCORRECT INPUT: blocked road node '{a}' not found")
            return
        if b not in all_nodes:
            print(f"INCORRECT INPUT: blocked road node '{b}' not found")
            return
        blocked.add((a, b))
        blocked.add((b, a))
        idx += 1
    
    # Пропускаем END (если есть)
    if idx < n and all_lines[idx].strip() == "END":
        idx += 1
    
    # ---------- 4. Добавляем обратные рёбра для съездов ----------
    edges_to_add = []
    for node, edges in list(graph.items()):
        for e in edges:
            if e.to.startswith("BH-"):
                has_reverse = False
                for rev in graph.get(e.to, []):
                    if rev.to == node:
                        has_reverse = True
                        break
                if not has_reverse:
                    edges_to_add.append((e.to, node, 1))
    
    for from_node, to_node, time_val in edges_to_add:
        graph[from_node].append(Edge(to_node, time_val))
        all_nodes.add(from_node)
    
    # ---------- 5. Поиск оптимального пути через J-1212 в J-24 ----------
    if "J-1212" not in all_nodes:
        print("INCORRECT INPUT: J-1212 not found in graph")
        return
    if "J-24" not in all_nodes:
        print("INCORRECT INPUT: J-24 not found in graph")
        return
    
    def dijkstra(start, target):
        if start not in graph:
            return None
        dist = {node: float('inf') for node in all_nodes}
        dist[start] = 0
        heap = [(0, start)]
        visited = set()
        
        while heap:
            d, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            if u == target:
                return d
            for e in graph.get(u, []):
                if (u, e.to) in blocked:
                    continue
                nd = d + e.time
                if nd < dist[e.to]:
                    dist[e.to] = nd
                    heapq.heappush(heap, (nd, e.to))
        return None
    
    best_time = float('inf')
    best_exit = None
    
    for ex in exits:
        if ex not in graph:
            continue
        time_to_1212 = dijkstra(ex, "J-1212")
        if time_to_1212 is None:
            continue
        time_1212_to_24 = dijkstra("J-1212", "J-24")
        if time_1212_to_24 is None:
            continue
        total = time_to_1212 + time_1212_to_24
        if total < best_time:
            best_time = total
            best_exit = ex
    
    if best_exit is None:
        print("INCORRECT INPUT: no valid path found")
        return
    
    total_with_home = best_time + 30
    print(f"{best_exit} {total_with_home}")

if __name__ == "__main__":
    solve()