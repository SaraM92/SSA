# SSA : Static Significance Analysis for Approximate Computing
Written by: Sara A. Metwalli
For Hara Lab in Tokyo Institute of Technology


#### This is v1.0 of SSA

The files in SSA:
-----------------
* Cleanup:
This file read the raw output of KLEE and clean up the information that is univalent to the analysis. E.g.:
-- KLEE output:
```
    KLEE: done: total instructions = 51 
    KLEE: done: completed paths = 3 
    KLEE: done: generated tests = 3   
    in case a = 0 >> z=: (Add w32 6 (Sub w32 (Mul w32 2 (ReadLSB w32 0 a)) (ReadLSB w32 0 c)))   
    in case a > 0 >> z=: (Add w32 (ReadLSB w32 0 a) (SDiv w32 (ReadLSB w32 0  b) 4))
    in case a < 0 >> z=: (Add w32 6 (Add w32 (SDiv w32 (ReadLSB w32 0 a)  2) (SDiv w32 (ReadLSB w32 0 b) 4)))
```
The first three lines of the output is not necessary for the analysis, so we need to remove such extra information, that's what the cleanup code does.

* Convert:
This file converts the result from *KQuery* (KLEE's constraint solver language) to readable math format to ease up the analysis algorithm. 

* Analyza:
This file performs the significance analysis on the converted result and then display the ranking out. The displayed information, such as the ranking or the detailed weights, can be controlled by the user by changing the script *analyze.py*.


Install SSA
-------------
1. Download and install KLEE from here.
For more information on KLEE and how it’s used, please visit this page.
2. Download SSA files and put it in the same directory as the files to be analyzed.

Before starting:
----------------
1.  KLEE only handles fixed-point operations, so, if the application has operations with non-fixed-point operators, the user needs to convert these operations into fixed-point first before inputting it to the tool. To read more about KLEE, please visit this website: http://klee.github.io/docs/

Using SSA:
-----------
1. Compile your C/C++ file into bitcode (.bc) file using clang/ llvm.
2. Loop iterations, the default in the tool now is 200 loops, however, the user can overwrite that using the “assume” function of KLEE to a range that fits.
3. Run KLEE on the input code and store the output to a text file “KLEEout_raw.txt
”.
4. Run SSA and wait for the ranking results to show up.

Published Paper:
---------------
Sara Ayman Metwalli and Yuko Hara-Azumi, "SSA-AC: Static Significance Analysis for Approximate Computing," ACM Transactions on Design Automation of Electronic Systems (TODAES), 2019.

For any questions or comments, please contact *ssa-ac@cad.ict.e.titech.ac.jp*
