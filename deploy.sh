#!/bin/bash
fission spec init
fission env create --spec --name get-ticker-env --image nexus.sigame.com.br/python-env-3.8:0.0.4 --builder nexus.sigame.com.br/python-builder-3.8:0.0.1
fission fn create --spec --name ticker-visual-fn --env get-ticker-env --src "./func/*" --entrypoint main.get_ticker_visual_identity
fission route create --spec --method GET --url /get_ticker --function ticker-visual-fn