from copy import deepcopy
import pandas
import json

def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '_' + key))
        elif isinstance(data, list):
            rows = []
            if (len(data) != 0):
                for i in range(len(data)):
                    [rows.append(elem) for elem in flatten_list(flatten_json(data[i], prev_heading))]
            else:
                data.append("")
                [rows.append(elem) for elem in flatten_list(flatten_json(data[0], prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pandas.DataFrame(flatten_json(data_in))


def remove_duplicates(df):
    columns = list(df)[:7]
    for c in columns:
        df[c] = df[c].mask(df[c].duplicated(), "")

    return df


if __name__ == '__main__':
    # data = {}
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = json_to_dataframe(data)
    # df = remove_duplicates(df)

    print(df)
    df.to_csv('data3.csv', index=False)
