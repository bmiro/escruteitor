# Usage for 28a.py

Prepare:

    pip3 install tabulate
    apt install espeak # For sound alarm

Execute:

    ./28a.py

If you want to persist the downloaded results issue:

    ./28a.py --persist

# Usage for 28aVeusProgressites.py

Execute it every 60s to check the results.

    watch -d -n 60 ./28aVeusProgressites.py

If you want a sound notification turn on your speakers and (check source code first ;) ):

    watch -d -n 60 ./28aVeusProgressites.py --sound

To tenerate HTML

    ./28aVeusProgressites.py --html





# Links

Results URL:
- https://resultados.eleccionesgenerales19.es

Results DATA:
- https://resultados.eleccionesgenerales19.es/json/CO/CO99999999999.json
- https://resultados.eleccionesgenerales19.es/assets/nomenclator.json
