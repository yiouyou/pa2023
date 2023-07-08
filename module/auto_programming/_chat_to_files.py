def is_chinese(_str):
    for ch in _str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def parse_chat(chat):  # -> List[Tuple[str, str]]:
    import re
    ##### Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)
    files = []
    for match in matches:
        path, code = "", ""
        # 在字符串中寻找 `image_resizer.py` 类型字符串
        _regex = r"\`(\w+\.\w+)\`"
        _m1 = re.findall(_regex, match.group(1))
        _m2 = list(set(_m1))
        if is_chinese(match.group(1)):
            if len(_m2) > 0:
                path = _m2[0]
        else:
            if len(_m2) > 0:
                path = _m2[0]
            else:
                # Strip the filename of any non-allowed characters and convert / to \
                path = re.sub(r'[<>"|?*]', "", match.group(1))
                # Remove leading and trailing brackets
                path = re.sub(r"^\[(.*)\]$", r"\1", path)
                # Remove leading and trailing backticks
                path = re.sub(r"^`(.*)`$", r"\1", path)
                # Remove trailing ]
                path = re.sub(r"\]$", "", path)
        # Get the code
        code = match.group(2)
        # Add the file to the list
        if path:
            files.append((path, code))
    ##### Get all the text except ```code``` block, 如果最后字符是 ':' or '：' 去掉最后一行
    readme = ""
    _split = chat.split("```")
    for i in range(0, len(_split), 2):
        _block = _split[i]
        if _block.endswith((':', '：')):
            _li = _block.split("\n")
            _block = "\n".join(_li)
        readme += _block
    files.append(("README.md", readme))
    return files


def to_files(chat, workspace):
    workspace["all_output.txt"] = chat
    files = parse_chat(chat)
    for file_name, file_content in files:
        workspace[file_name] = file_content

