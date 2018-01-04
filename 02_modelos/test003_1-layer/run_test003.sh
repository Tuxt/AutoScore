#!/bin/bash
#python test003_1-layer.py --layer SimpleRNN --max-timesteps 50  --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/abc/dataset1_clean.abc &&
python test003_1-layer.py --layer SimpleRNN --max-timesteps 50  --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado &&
python test003_1-layer.py --layer SimpleRNN --max-timesteps 100 --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado &&
python test003_1-layer.py --layer LSTM      --max-timesteps 50  --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado &&
python test003_1-layer.py --layer LSTM      --max-timesteps 100 --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado &&
python test003_1-layer.py --layer GRU       --max-timesteps 50  --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado &&
python test003_1-layer.py --layer GRU       --max-timesteps 100 --rnn-units 64 --batch-size 64 --epochs 20 --verbosity 6 /home/tuxt/tfg/code/abc_code/01_preproceso/codes/archivo_salida_arreglado
