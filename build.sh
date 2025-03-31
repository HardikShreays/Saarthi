#!/bin/bash
pip install -r ./server/requirements.txt
cd client/Saarthi
npm install
npm run build
cd ../..