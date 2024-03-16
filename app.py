from copy import deepcopy
from typing import Union
from time import time
from flask import Flask, request, jsonify

orig_seed = time()

app = Flask(__name__)

@app.route('/solve/<uuid>', methods=['GET', 'POST'])
def api_request(uuid):
    content = request.json
    table = content['table']
    solved = riesitel(tabulka=table)
    #print(*solved[0], sep='\n')
    return jsonify({"uuid":uuid, 'solved':solved})


def riesitel(tabulka: list[list[int]], mode: int=1, max_depth: int=30) -> Union[list[list[list[int]]], list[list[set[int]]]]:
    if max_depth == 0:
        raise Exception('Recursion too deep.')
    moznosti = [[set([i for i in range(1,10)]) for x in range(9)] for y in range(9)]
    kopia = deepcopy(tabulka)

    for iy, y in enumerate(tabulka):
        for ix, x in enumerate(y):
            if x !=0:
                for mx in range(9):
                    moznosti[iy][mx].discard(x)
                for my in range(9):
                    moznosti[my][ix].discard(x)
                for my in range(3):
                    for mx in range(3):
                        moznosti[my + (iy//3)*3][mx + (ix//3)*3].discard(x)
                moznosti[iy][ix] = {x}
    #print(*moznosti, sep='\n')

    for iy, y in enumerate(moznosti):
        pocet_moznych = []
        for x in y:
            pocet_moznych += list(x)
        for n in range(1, 10):
            if pocet_moznych.count(n) == 1:
                for ix in range(9):
                    if n in moznosti[iy][ix]:
                        moznosti[iy][ix] = {n}
    
    for ix in range(9):
        pocet_moznych = []
        for iy in range(9):
            pocet_moznych += list(moznosti[iy][ix])
        for n in range(1, 10):
            if pocet_moznych.count(n) == 1:
                for iy in range(9):
                    if n in moznosti[iy][ix]:
                        moznosti[iy][ix] = {n}

    for iy in range(0, 9, 3):
        for ix in range(0, 9, 3):
            pocet_moznych = []
            for iy2 in range(3):
                for ix2 in range(3):
                    pocet_moznych += list(moznosti[iy + iy2][ix + ix2])
            for n in range(1, 10):
                if pocet_moznych.count(n) == 1:
                    for iy2 in range(3):
                        for ix2 in range(3):
                            if n in moznosti[iy + iy2][ix + ix2]:
                                moznosti[iy + iy2][ix + ix2] = {n}
    
    for iy, y in enumerate(moznosti):
        for ix, x in enumerate(y):
            if len(x) == 1:
                tabulka[iy][ix] = list(x)[0]
                

    if kopia == tabulka:
        if mode == 2:
            return moznosti
        for iy, y in enumerate(deepcopy(moznosti)):
            for ix, x in enumerate(y):
                riesenia = []
                if len(x) == 0:
                    return []
                elif len(x) != 1:
                    for n in x:
                        tabulka[iy][ix] = n
                        riesenia.extend(riesitel(tabulka=deepcopy(tabulka), max_depth=max_depth-1))
                    moznosti = None
                    return riesenia
        moznosti = None
        return [tabulka]
    return riesitel(tabulka=tabulka, mode=mode, max_depth=max_depth-1)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
