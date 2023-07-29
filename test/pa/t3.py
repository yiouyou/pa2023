from pathlib import Path
import re
import pprint as pp

chat_cn = Path("t3_chat_cn.txt").absolute().read_text()
# print(chat_cn)
chat_en = Path("t3_chat_en.txt").absolute().read_text()

def is_chinese(_str):
    for ch in _str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def parse_chat(chat):  # -> List[Tuple[str, str]]:
    # Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        # print(f"match:{match}")
        print(f"match.group(1):{match.group(1)}")
        # print(f"match.group(2):{match.group(2)}")

        if is_chinese(match.group(1)):
            # 在中文字符串中寻找 `image_resizer.py` 类型字符串
            _regex = r"\`(\w+\.\w+)\`"
            _m1 = re.findall(_regex, match.group(1))
            _m2 = list(set(_m1))
            if len(_m2) > 0:
                path = _m2[0]
            else:
                path = ""
        else:
            # Strip the filename of any non-allowed characters and convert / to \
            path = re.sub(r'[<>"|?*]', "", match.group(1))
            # Remove leading and trailing brackets
            path = re.sub(r"^\[(.*)\]$", r"\1", path)
            # Remove leading and trailing backticks
            path = re.sub(r"^`(.*)`$", r"\1", path)
            # Remove trailing ]
            path = re.sub(r"\]$", "", path)
            # Remove trailing :
            path = re.sub(r"\:$", "", path)

        # Get the code
        code = match.group(2)

        # Add the file to the list
        if path:
            files.append((path, code))

    # Get all the text before the first ``` block
    readme = chat.split("```")[0]
    files.append(("README.md", readme))

    # Return the files
    return files

_cn = parse_chat(chat_cn)
# print(type(_cn))
pp.pprint(_cn)

_en = parse_chat(chat_en)
# print(type(_en))
pp.pprint(_en)

