#!/usr/bin/env python3

import os
import json
import urllib.request

from sys import argv
from datetime import datetime

# apt install python3-tabulate || pip3 install tabulate
from tabulate import tabulate

RESULTS_URL = "https://resultados.eleccionesgenerales19.es/json/CO/CO99999999999.json"
NAMES_URL = "https://resultados.eleccionesgenerales19.es/assets/nomenclator.json"
RESULTS_JOURNAL_DIR = "results-28a2019"

RESULTS_KEY = "act" # act -> current reults, ant -> for 2016 results
SEATS_THRESHOLD = -1 # Show only parties with more than SEATS_THRESHOLD

def get_party_name(names_data, party_code):
    """
    " @return party name given the party code
    """
    for party in names_data["partidos"]["co"][RESULTS_KEY]:
        if party["codpar"] == party_code:
            return party["nombre"]
    return "????????"


if __name__=="__main__":
    print("Elecciones Generales 2019 28A\n")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Getting data
    results_raw = urllib.request.urlopen(RESULTS_URL).read().decode('utf-8')
    names_raw = urllib.request.urlopen(NAMES_URL).read().decode('utf-8')

    if "--persist" in argv:
        # Persist data as journal
        results_data_file = "{}/results-raw-{}.json".format(
            RESULTS_JOURNAL_DIR,
            timestamp,

        )
        names_file = "{}/names-raw-{}.json".format(
            RESULTS_JOURNAL_DIR,
            timestamp,
        )

        if not os.path.isdir(RESULTS_JOURNAL_DIR):
            os.mkdir(RESULTS_JOURNAL_DIR)

        for filename in (results_data_file, names_file):
            with open(filename, 'w') as f:
                f.write(results_raw)

    # Print seat results
    results_data = json.loads(results_raw)
    names_data = json.loads(names_raw)

    results = {}

    for party_result in results_data["partotabla"]:
        party_code = party_result[RESULTS_KEY]["codpar"]
        party_seats = int(party_result[RESULTS_KEY]["carg"])
        if party_seats > SEATS_THRESHOLD:
            results[party_code] = party_seats

    table = []
    for r in sorted(results.items(), key=lambda kv: int(kv[1]), reverse=True):
        party_code = r[0]
        party_seats = r[1]
        party_name = get_party_name(names_data, party_code)
        table.append((party_seats, party_name))

    print("Actualizado: {}".format(datetime.now().strftime("%H:%M")))
    print("Escrutado: {}".format(results_data["totales"]["act"]["pmesesc"]))
    print(tabulate(table))
