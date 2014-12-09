#!/usr/bin/env bash
rm ../episodes.db
rm episodes.db
../manage.py syncdb 
./provision-data.py
cp episodes.db ../
