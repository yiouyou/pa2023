from time import sleep


def get_config(_key):
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _config_path = _pwd.parent.parent
    import os
    _json = os.path.join(_config_path, "config.json")
    # print(_json)
    import json
    with open(_json, "r") as jf:
        _config = json.load(jf)
    return _config[_key]


def timestamp_now():
    import time
    current_GMT = time.gmtime()
    import calendar
    ts = calendar.timegm(current_GMT)
    return ts


def parse_intermediate_steps(_list):
    _steps = []
    for n in range(len(_list)):
        i = _list[n]
        i_str = f"Step {n+1}: {i[0].tool}\n"
        i_str += f"> {i[0].tool_input}\n"
        i_str += f"< {i[0].log}\n"
        i_str += f"# {i[1]}\n"
        _steps.append(i_str)
    return "\n".join(_steps)

