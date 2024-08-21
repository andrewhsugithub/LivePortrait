#!/bin/bash

echo "source /mnt/Nami/users/Jason0411202/anaconda3/bin/activate"
source /mnt/Nami/users/Jason0411202/anaconda3/bin/activate
echo "conda activate LivePortrait"
conda activate LivePortrait
echo "python app.py --flag_do_torch_compile --loop"
python app.py --flag_do_torch_compile --loop