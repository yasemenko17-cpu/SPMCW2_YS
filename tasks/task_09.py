import re

def solve(source: str) -> list:
    lines = source.split("\n")
    messages = []
    
    lib_name = None
    defined_argtypes = set()
    defined_restype = set()
    buffers = {} # ім'я буфера -> розмір
    
    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Пошук ініціалізації бібліотеки
        lib_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:ctypes\.)?CDLL\(", line)
        if lib_match:
            lib_name = lib_match.group(1)
            continue
            
        # Пошук створення буфера
        if "create_string_buffer" in line and "=" in line:
            try:
                b_name = line.split("=")[0].strip()
                size_str = line.split("create_string_buffer(")[1].split(")")[0].strip()
                if size_str.isdigit():
                    buffers[b_name] = int(size_str)
            except Exception:
                pass

        # Фіксація argtypes та restype
        if lib_name and f"{lib_name}." in line:
            if ".argtypes" in line:
                func_part = line.split(".argtypes")[0]
                func_name = func_part.replace(f"{lib_name}.", "").strip()
                defined_argtypes.add(func_name)
            if ".restype" in line:
                func_part = line.split(".restype")[0]
                func_name = func_part.replace(f"{lib_name}.", "").strip()
                defined_restype.add(func_name)

        # Пошук будь-яких викликів функцій бібліотеки (навіть якщо є присвоєння типу p = libc.malloc(...))
        if lib_name and f"{lib_name}." in line and "argtypes" not in line and "restype" not in line:
            # Знаходимо всі входження викликів lib.func(...) у рядку
            calls = re.findall(rf"{lib_name}\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)", line)
            for func_name, args_content in calls:
                # Правило 1: відсутність argtypes
                if func_name not in defined_argtypes:
                    messages.append((idx, 1, f"Рядок {idx}: у {lib_name}.{func_name} не задано argtypes"))
                    defined_argtypes.add(func_name)
                
                # Правило 2: відсутність restype для функцій, що повертають вказівник
                ptr_returning_funcs = {'malloc', 'calloc', 'realloc', 'strdup', 'getenv', 'getcwd', 'mmap', 'fopen', 'strerror', 'strchr', 'strstr'}
                if func_name in ptr_returning_funcs and func_name not in defined_restype:
                    messages.append((idx, 2, f"Рядок {idx}: у {lib_name}.{func_name} не задано restype (повертає вказівник; ctypes припускає int)"))
                    defined_restype.add(func_name)

                # Правило 3 для memcpy
                if func_name == "memcpy":
                    args = [arg.strip() for arg in args_content.split(",")]
                    if len(args) >= 3:
                        target_buf = args[0]
                        size_arg = args[2]
                        if size_arg.isdigit():
                            written_size = int(size_arg)
                            if target_buf in buffers and written_size > buffers[target_buf]:
                                messages.append((idx, 3, f"Рядок {idx}: memcpy може записати {written_size} байтів у буфер {target_buf} розміром {buffers[target_buf]}"))

    # Сортування: спершу за номером рядка, потім за номером правила
    messages.sort(key=lambda x: (x[0], x[1]))
    return [m[2] for m in messages]