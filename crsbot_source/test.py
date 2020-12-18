from . import get_json
#from .log import logger

def test():
    get_json.save_and_return_json("https://chunithm.sega.jp/data/common.json", "domestic")

if __name__ == "__main__":
    test()