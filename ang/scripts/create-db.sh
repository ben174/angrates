#!/usr/bin/env bash
rm ../tools.db
rm tools.db
../manage.py syncdb 
./provision-data.py
cp tools.db ../
