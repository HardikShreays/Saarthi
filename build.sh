#!/bin/bash
pip install -r ./server/requirements.txt
cd client
npm install
npm run build
cd ..