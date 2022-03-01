# DSP
#### in order to run hw#1.py
-   install `arabic_reshaper` and `hazm`
-   in order to use hazm you need also to install `wapiti` via `sudo apt install wapiti`
-   install `sox` via `sudo apt install sox`
-   run `python3 hw#1.py` in terminal with one of the following arguments [`--number`, `--number_phoneme`], [`--persian_sentence`, `--persian_sentence_phoneme`], [`--pesian_number`, `--persian_number_phoneme`].
 
**examples**
```
    python3 hw#1.py --number 
2409
    python3 hw#1.py --number_phoneme 
2409

    python3 hw#1.py --persian_number "دویست و دو هزار و ده"
    python3 hw#1.py --persian_number_phoneme "دویست و دو هزار و ده"

    python3 hw#1.py --persian_sentence "دانشگاه تهران"
    python3 hw#1.py --persian_sentence_phoneme "دانشگاه تهران"
```

---