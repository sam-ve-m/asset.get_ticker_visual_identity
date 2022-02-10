#!/bin/bash
fission spec init
fission env create --spec --name get-ticker --image fission/python-env --builder fission/python-builder
fission fn create --spec --name get-ticker --env get-ticker --src "func/*" --entrypoint main.get_ticker_visual_identity
fission route create --spec --method GET --url /get_ticker_visual_identity --function get-ticker