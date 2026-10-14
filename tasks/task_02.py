def solve(address: int, length: int, page_size: int) -> str:
    # Перевірка, чи page_size є додатним степенем двійки
    if page_size <= 0 or (page_size & (page_size - 1)) != 0:
        return "Помилка: розмір сторінки має бути степенем двійки"
    if address < 0:
        return "Помилка: адреса не може бути від'ємною"
    if length < 1:
        return "Помилка: довжина має бути додатною"

    start_page = address // page_size
    end_address = address + length - 1
    end_page = end_address // page_size
    num_pages = end_page - start_page + 1
    offset = address % page_size
    
    page_start_addr = start_page * page_size
    hex_addr = hex(page_start_addr)
    
    covered = num_pages * page_size
    unused = covered - length

    return (
        f"сторінок: {num_pages} (від {start_page} до {end_page}); "
        f"зсув у першій: {offset}; початок першої: {hex_addr}; "
        f"покрито: {covered} Б, не використано: {unused} Б"
    )