# [CZ] Návod ke spuštění programu

> @autor Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>

> @datum 8/5/2023

Tento návod slouží ke zprovoznění programů stromového a lineárního genetického programování. Je platný pro obě varianty.
Nejprve je ale potřeba si doinstalovat potřebné knihovny, které jsou uvedené v souboru requirements.txt.

Programy se nacházi ve složce src/, kde se následně nachází dvě složky s těmito programy TGP/ a LGP/.

Spouští se následujícím příkazem:

```
$ python3 main.py 
```

K modifikaci inicializačních parametrů programu slouží primárně soubor init_params.py.

K paralelnímu spuštění více běhů zároveň je třeba upravit hodnotu NUM_OF_RUNS na spodku souboru main.py.

Pokud je potřeba měnit při opakovaném spuštění parametry velikosti populace, pravděpodbnosti křížení a mutace lze to úpravou hodnot parametrů ve funkci run_gp, která se opět nachází na spodku souboru main.py. 

```
run_gp(fns, pop_size=1, cross_rate=1, mut_rate=1) 
```

Ještě navíc je potřeba povolit hodnotou True aplikaci těchto parametrů při volání funkce parallel_computing opět v souboru main.py.

Ke změně stezky mravence je potřeba ji nastavit ve složce trail_plots.py u komentáře "CHOOSE TRAIL TO RENDER HERE"  (dtto v main.py, řádek LGP 128/TGP 98 a gif.py, řádek 78) a následně nastavit i správnou velikost mřížky v init_params.py.

# [EN] Instructions for running the program

> @author Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>

> @date 8/5/2023

This tutorial is for running tree and linear genetic programming programs. It is valid for both variants.
But first you need to install the necessary libraries, which are listed in the requirements.txt file.

The programs are located in the src/ folder, which then contains the two folders containing these programs, TGP/ and LGP/.

They are started with the following command:

```
$ python3 main.py 
```

The init_params.py file is primarily used to modify program initialization parameters.

To run multiple runs in parallel at the same time, the NUM_OF_RUNS value at the bottom of the main.py file must be modified.

If the population size, crossover probability, and mutation parameters need to be changed during repeated runs, this can be done by editing the parameter values in the run_gp function, again located at the bottom of the main.py file. 

```
run_gp(fns, pop_size=1, cross_rate=1, mut_rate=1) 
```

Additionally, you need to enable the True value to apply these parameters when calling the parallel_computing function, again in the main.py file.

To change the ant's trail, you need to set it in trail_plots.py at the "CHOOSE TRAIL TO RENDER HERE" comment (dtto in main.py, line  LGP 128/TGP 98  and gif.py, line 78) and then set the correct grid size in init_params.py.