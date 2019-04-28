#!/usr/bin/env python3

import os
import json
import urllib.request

from datetime import datetime

SOUND_NOTIFICATION = "espeak"
RESULTS_URL = "https://resultados.eleccionesgenerales19.es/json/CO/CO99999999999.json"
NAMES_URL = "https://resultados.eleccionesgenerales19.es/assets/nomenclator.json"
RESULTS_JOURNAL_DIR = "results-28a2019"


def get_party_name(names_data, party_code):
    """
    " @return party name given the party code
    """
    for party in names_data["partidos"]["co"]["ant"]:
        if party["codpar"] == party_code:
            return party["nombre"]

    return "????????"


if __name__=="__main__":
    print("Elecciones Generales 2019 28A\n")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    print("Getting data...")
    results_raw = urllib.request.urlopen(RESULTS_URL).read().decode('utf-8')
    names_raw = urllib.request.urlopen(NAMES_URL).read().decode('utf-8')

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

    print("Persistng journal data...")
    for filename in (results_data_file, names_file):
        with open(filename, 'w') as f:
            f.write(results_raw)

    results_data = json.loads(results_raw)
    names_data = json.loads(names_raw)

    total_results = {}

    print("\n\n")
    print("Escrutado: {}".format(results_data["totales"]["act"]["pmesesc"]))

    for party_result in results_data["partotabla"]:
        party_code = party_result["ant"]["codpar"]
        party_seats = int(party_result["ant"]["carg"])
        if party_seats > 0:
            party_name = get_party_name(names_data, party_code)
            total_results[party_name] = party_result["ant"]["carg"]

    print(total_results)

