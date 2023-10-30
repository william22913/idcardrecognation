import re
import string


def read_value_or_key(_val: string, queue_field, queue_value, result):
    split_eq = _val.strip().split("=")
    if len(split_eq) > 1:
        if split_eq[0] != '' and split_eq[1] != '':
            result[split_eq[0].strip(" ")] = split_eq[1].strip(" ")
            return

    split_eq = _val.strip().split(":")
    if len(split_eq) > 1:
        if split_eq[0] != '' and split_eq[1] != '':
            result[split_eq[0].strip(" ")] = split_eq[1].strip(" ")
            return
    capture = _val
    _val = _val.replace("=", "")
    _val = _val.replace(":", "")
    _val = _val.strip()
    if _val == "NIK" or "RT/" in _val or "/RW" in _val:
        queue_field.append(_val)
    elif "Gol Darah" in _val:
        splitted = _val.split("Gol Darah")
        if len(splitted) > 1:
            if splitted[1].strip(" ") != '':
                result['Gol Darah'] = splitted[1].strip(" ")
    elif "Gol. Darah" in _val:
        splitted = _val.split("Gol. Darah")
        if len(splitted) > 1:
            if splitted[1].strip(" ") != '':
                result['Gol. Darah'] = splitted[1].strip(" ")
    elif _val.isupper() or _val.replace("/", "").replace("-", "").replace(" ", "").strip(" ").isnumeric():
        if _val.replace(".", "").replace(" ", "").isalpha() or re.search("[0-9]+-[0-9]+-[0-9]+$", _val):
            capture = ": " + _val

        if 'PROVINSI' in _val:
            province = _val.replace('PROVINSI', '').replace(':', '').strip()
            result["Provinsi"] = province
            return
        elif 'KABUPATEN' in _val or 'KOTA' in _val:
            city = _val.replace('KABUPATEN', '').replace('KOTA', '').replace('JAKARTA', '').replace(':', '').strip()
            result["Kabupaten/Kota"] = city
            return
        elif 'JAKARTA' in _val and re.search("[0-9]+-[0-9]+-[0-9]+$", _val) is None:
            city = _val.replace('JAKARTA', '').replace(':', '').strip()
            result["Kabupaten/Kota"] = "JAKARTA "+city
            return
        elif _val == 'PEREMPUAN' or _val == 'LAKI-LAKI':
            queue_value.append(_val)
            return

        if ":" in capture or len(_val) <= 3 or len(_val) >= 5 and _val.isalpha():
            queue_value.append(_val)
        elif _val.replace("/", "").replace("-", "").replace(" ", "").strip(" ").isnumeric():
            queue_value.append(_val)
        else:
            if len(queue_value) > 0:
                appended_value = queue_value.pop()
                if appended_value.isnumeric() == _val.isnumeric() and appended_value.isupper() == _val.isupper():
                    temp = appended_value+" "+_val
                    if len(temp) <= 25:
                        queue_value.append(temp)
                    else:
                        queue_value.append(appended_value)
                        queue_value.append(_val)
                else:
                    queue_value.append(appended_value)
                    queue_value.append(_val)
            else:
                queue_value.append(_val)
    else:
        queue_field.append(_val)


def combine_value_and_field(queue_field, queue_value, result):
    while len(queue_field) > 0:
        field = queue_field.pop(0)

        if len(queue_value) > 0:
            value = queue_value.pop(0)
            if field == 'Gol. Darah':
                match value:
                    case 'A', 'B', '0', 'AB', 'O', '-':
                        result[field] = value
                    case _:
                        result[field] = '-'
                        queue_value.insert(0, value)
            else:
                result[field] = value
        else:
            result[field] = "-"

        # print(result)


def read_google_vision_result(param: string):
    result = {}
    queue_field = []
    queue_value = []

    val = param.split("\n")

    for i in val:
        read_value_or_key(i, queue_field, queue_value, result)

    combine_value_and_field(queue_field, queue_value, result)

    return result
