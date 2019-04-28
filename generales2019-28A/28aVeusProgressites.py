#!/usr/bin/env python3

import os
import json
import urllib.request

from sys import argv
from datetime import datetime

# apt install python3-tabulate || pip3 install tabulate
from tabulate import tabulate

RESULTS_URL = "https://resultados.eleccionesgenerales19.es/json/CO/CO04999999999.json"
NAMES_URL = "https://resultados.eleccionesgenerales19.es/assets/nomenclator.json"

RESULTS_KEY = "act" # act -> current reults, ant -> for 2016 results
TARGET_PARTY = "0006" # Veus PROGRESSISTES

SEATS = 8

HTML = """
<html>
  <head>
    <title>Eleccions Generals 2019 28A - Habemus diputat?</title>
    <meta http-equiv=”refresh” content=”60" />
     <meta charset="utf-8">
  </head>

  <body>
    <h1>Eleccions Generals 2019 28A - Habemus diputat?</h1>
    <p>Actualitzat: {updated}</p>
    <p>Escrutat: {escrutat}</p>

    <pre>
{table}
    </pre>

    <p>Llindar d'escó: {threshold}</p>
    <p>{target_party}: {party_votes}</p>

    <b>{message}</b>
  </body>
</html>
"""


def get_party_name(names_data, party_code):
    """
    " @return party name given the party code
    """
    for party in names_data["partidos"]["co"][RESULTS_KEY]:
        if party["codpar"] == party_code:
            return party["siglas"]
    return "????????"


if __name__=="__main__":

    results_raw = urllib.request.urlopen(RESULTS_URL).read().decode('utf-8')
    names_raw = urllib.request.urlopen(NAMES_URL).read().decode('utf-8')

    results_data = json.loads(results_raw)
    names_data = json.loads(names_raw)

    target_name = get_party_name(names_data, TARGET_PARTY)
    target_votes = 0

    results = {}

    has_seat = False
    for party_result in results_data["partotabla"]:
        party_code = party_result[RESULTS_KEY]["codpar"]
        party_seats = int(party_result[RESULTS_KEY]["carg"])
        party_votes = int(party_result[RESULTS_KEY]["vot"])
        if party_code == TARGET_PARTY:
            target_votes = party_votes
            has_seat = True
        results[party_code] = {
            "seats": party_seats,
            "votes": party_votes,
        }


    seats_column = 1
    seats_calculs_start_column = 3
    headers = ["Partit", "Escons", "Vots"] + [ str(i) for i in range(1, SEATS + 1) ]
    matrix = []
    hondt = []
    for party_code, result in results.items():
        votes = result["votes"]
        matrix_line = [ party_code, 0, votes]
        for seat in range(1, SEATS + 1):
            calculus = int(votes / seat)
            hondt.append(
                (party_code, calculus, seat)
            )
            matrix_line.append(calculus)
        matrix.append(matrix_line)

    hondt = sorted(hondt, key=lambda x: x[1], reverse=True)[:8]

    # Seats calculus
    for party_code in results.keys():
        i = 0
        for row in matrix:
            if row[0] == party_code:
                seats = len([x for x in filter(lambda x: x[0] == party_code, hondt)])
                matrix[i][seats_column] = seats
                break
            i += 1

    # Mark seats
    for hondt_seat in hondt:
        party_code = hondt_seat[0]
        seat = hondt_seat[2]
        i = 0
        for row in matrix:
            if row[0] == party_code:
                j = seats_calculs_start_column -1 + seat
                value = matrix[i][j]
                matrix[i][j] = ">> {} <<".format(value)
            i += 1

    # Finding threshold
    seat_threshold = hondt[-1][1]

    # Set party names
    for row in matrix:
        row[0] = get_party_name(names_data, row[0])


    if target_votes > seat_threshold:
        msg = "Fumata negra! Habemus diputat! (de moment)"
    else:
        msg = "Diputat en proces... :("

    if "--html" in argv:
        print(
            HTML.format(
                updated=datetime.now().strftime("%H:%M"),
                escrutat=results_data["totales"]["act"]["pmesesc"],
                table=tabulate(matrix, headers=headers),
                threshold=seat_threshold,
                target_party=target_name,
                party_votes=target_votes,
                message=msg,
            )
        )
    else:
        print("Eleccions Generals 2019 28A - Habemus diputat?\n")
        print("Actualitzat: {}".format(datetime.now().strftime("%H:%M")))
        print("Escrutat: {}\n".format(results_data["totales"]["act"]["pmesesc"]))
        print(tabulate(matrix, headers=headers))
        print("\nLlindar d'escó: {} vots".format(seat_threshold))
        print("{}: {} vots".format(target_name, target_votes))
        print("\n\n\n\nCodi font: https://github.com/bmiro/escruteitor/tree/master/generales2019-28A")

    if "--sound" in argv:
        if target_votes > seat_threshold:
            for i in range(3):
                os.system("echo '{}' | espeak".format(msg))
        else:
            os.system("echo '{}' | espeak".format(msg))
