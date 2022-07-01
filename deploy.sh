#!/bin/bash
fission spec init
fission env create --spec --name get-ticker-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name ticker-visual-fn --env get-ticker-env --src "./func/*" --entrypoint main.get_ticker_visual_identity
fission route create --name get-ticker-visual-identity --spec --method GET --url /get-ticker-visual-identity --function ticker-visual-fn