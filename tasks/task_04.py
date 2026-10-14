def solve(current: tuple, new: tuple, privileged: bool) -> str:
    def val_to_cmp(v):
        return float('inf') if v == -1 else v

    def fmt_val(v):
        return "необмежено" if v == -1 else str(v)

    soft_new, hard_new = new

    # 1. Перевірка на від'ємні значення (окрім -1) та м'який > жорсткий
    if any(x < -1 for x in new) or val_to_cmp(soft_new) > val_to_cmp(hard_new):
        return "EINVAL"

    # 2. Перевірка для непривілейованого процесу (збільшення жорсткого ліміту)
    if not privileged and val_to_cmp(hard_new) > val_to_cmp(current[1]):
        return "EPERM"

    return f"OK: м'який={fmt_val(soft_new)}, жорсткий={fmt_val(hard_new)}"