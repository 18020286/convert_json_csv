import json
import pandas


if __name__ == '__main__':
    print('hello')
    with open("sample2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data)