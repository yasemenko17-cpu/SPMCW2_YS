import collections

def solve(objects: list, refs: list, variables: list, delete: list) -> tuple:
    obj_set = set(objects)
    
    # Перевірка невідомих об'єктів у refs та variables
    for a, b in refs:
        if a not in obj_set:
            raise ValueError(f"Невідомий об'єкт: {a}")
        if b not in obj_set:
            raise ValueError(f"Невідомий об'єкт: {b}")
            
    for v in variables:
        if v not in obj_set:
            raise ValueError(f"Невідомий об'єкт: {v}")
            
    # Перевірка і видалення змінних
    var_counts = collections.Counter(variables)
    for d in delete:
        if var_counts[d] > 0:
            var_counts[d] -= 1
        else:
            raise ValueError(f"Немає змінної: {d}")

    # Побудова посилань
    in_refs_from_objs = collections.default_int = collections.defaultdict(int)
    for a, b in refs:
        in_refs_from_objs[b] += 1

    current_ref_counts = {}
    for obj in objects:
        current_ref_counts[obj] = var_counts[obj] + in_refs_from_objs[obj]

    # Симуляція звільнення за лічильником посилань (refcount == 0)
    freed = set()
    queue = [obj for obj in objects if current_ref_counts[obj] == 0]

    # Зберігаємо вихідні зв'язки для зменшення лічильників цілей
    outgoing = collections.defaultdict(list)
    for a, b in refs:
        outgoing[a].append(b)

    while queue:
        curr = queue.pop(0)
        if curr in freed:
            continue
        freed.add(curr)
        for target in outgoing[curr]:
            if target not in freed:
                current_ref_counts[target] -= 1
                if current_ref_counts[target] == 0:
                    queue.append(target)

    # Визначення живих об'єктів (досяжних від змінних, що лишилися)
    active_vars = [obj for obj, cnt in var_counts.items() if cnt > 0 and obj not in freed]
    alive = set()
    visited = set(active_vars)
    q_alive = list(active_vars)
    
    while q_alive:
        curr = q_alive.pop(0)
        alive.add(curr)
        for target in outgoing[curr]:
            if target not in freed and target not in visited:
                visited.add(target)
                q_alive.append(target)

    freed_list = [o for o in objects if o in freed]
    alive_list = [o for o in objects if o in alive]
    garbage_list = [o for o in objects if o not in freed and o not in alive]

    return (freed_list, alive_list, garbage_list)