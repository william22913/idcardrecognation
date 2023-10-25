import re
import string


def read_value_or_key(_val: string):
    splitedEq = _val.strip().split("=")
    if len(splitedEq) > 1:
        if splitedEq[0] != '' and splitedEq[1] != '':
            result[splitedEq[0].strip(" ")] = splitedEq[1].strip(" ")
            return

    splitedEq = _val.strip().split(":")
    if len(splitedEq) > 1:
        if splitedEq[0] != '' and splitedEq[1] != '':
            result[splitedEq[0].strip(" ")] = splitedEq[1].strip(" ")
            return
    capture = _val
    _val = _val.replace("=", "")
    _val = _val.replace(":", "")
    _val = _val.strip()
    if _val == "NIK" or "RT/" in _val or "/RW" in _val:
        queueField.append(_val)
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
            queueValue.append(_val)
            return

        if ":" in capture or len(_val) <= 3 or len(_val) >= 5 and _val.isalpha():
            queueValue.append(_val)
        elif _val.replace("/", "").replace("-", "").replace(" ", "").strip(" ").isnumeric():
            queueValue.append(_val)
        else:
            if len(queueValue) > 0:
                appended_value = queueValue.pop()
                if appended_value.isnumeric() == _val.isnumeric() and appended_value.isupper() == _val.isupper():
                    temp = appended_value+" "+_val
                    if len(temp) <= 25:
                        queueValue.append(temp)
                    else:
                        queueValue.append(appended_value)
                        queueValue.append(_val)
                else:
                    queueValue.append(appended_value)
                    queueValue.append(_val)
            else:
                queueValue.append(_val)
    else:
        queueField.append(_val)


def combine_value_and_field():
    while len(queueField) > 0:
        field = queueField.pop(0)

        if len(queueValue) > 0:
            value = queueValue.pop(0)
            if field == 'Gol. Darah':
                match value:
                    case 'A', 'B', '0', 'AB', 'O', '-':
                        result[field] = value
                    case _:
                        result[field] = '-'
                        queueValue.insert(0, value)
            else:
                result[field] = value
        else:
            result[field] = "-"

        print(result)


example = 'NIK\nNama\nTempat/Tgl Lahir\nJenis Kelamin\nAlamat\nRT/RW\nKel/Desa\nKecamatan\nPROVINSI DKI ' \
          'JAKARTA\nJAKARTA SELATAN\n3174096112900001\n: DEBBY ANGGRAINI\n: JAKARTA, 21-12-1990\n: PEREMPUAN\n: JL ' \
          'KECAPI V\n: 006 / 005\n: JAGAKARSA\n: JAGAKARSA\n: ISLAM\nAgama\nStatus Perkawinan: BELUM ' \
          'KAWIN\nPekerjaan\nKewarganegaraan:\nBerlaku Hingga\nGol. Darah :\n: KARYAWAN SWASTA\nWNI\n: 21-12-2016 '

last = ''
result = {}
queueField = []
queueValue = []
val = example.split("\n")

for i in val:
    read_value_or_key(i)

combine_value_and_field()