import json
import os
import collections


def bfs(graph, root):
    visited = list()
    types = dict()
    try:
        while root:
            visited.append(root[0])
            if isinstance(graph[root[0]], str):
                visited.append(graph[root[0]])
            elif isinstance(graph[root[0]], dict):
                for i in graph[root[0]].keys():
                    types[i] = graph[root[0]].get(i, None)
            else:
                for neighbour in graph[root[0]]:
                    visited.append(neighbour)
            root.pop(0)
    except IndexError:
        pass

    return visited, types


with open('schema/label_selected.schema', 'r') as file:
    schema_file = json.load(file)

graph = schema_file
structure, types = bfs(graph, list(graph.keys()))

with open('event/ba25151c-914f-4f47-909a-7a65a6339f34.json') as file:
    json_file = json.load(file)

dict_for_compare = {}


def compare_required(json_file, schema_file):
    required = schema_file.get('required')
    data = list(json_file.get('data').keys())
    result = [key for key in required if key not in data]
    if result:
        print(f'In JSON file no fields {result}')
        for res in result:
            print(f'Please add field {res}')
            print(f'{res} must be {schema_file["properties"].get(res)}')
    else:
        print(f'JSON file is fine')


def get_required(file):
    required = file.get('required')
    print(required)


def get_keys(file):
    keys = file.keys()
    print(keys)


def get_properties(file):
    properties = file.get('properties')
    return properties


def compare_types(json_file, schema_file):
    # filetypes = list(schema_file['properties'].values())
    schema_keys = list(schema_file['properties'].keys())
    json_keys = list(json_file['data'].keys())
    schema_types = [schema_file['properties'].get(i)['type'] for i in schema_keys]
    json_types = [type(json_file['data'].get(i)) for i in json_keys]

    return json_types, schema_types


if __name__ == '__main__':
    # compare_required(json_file, schema_file)
    # get_properties(schema_file)
    print(compare_types(json_file, schema_file))
