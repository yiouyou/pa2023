from _util import generate_sku


if __name__ == "__main__":

    import sys, os
    _dir = sys.argv[1]
    _fn = sys.argv[2]
    _path = os.path.join(_dir, _fn)
    with open(_path, 'r', encoding='utf-8') as rf:
      _info = rf.read()
    generate_sku(_info, _dir, _fn)

