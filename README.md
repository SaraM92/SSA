# SSA : Static Significance Analysis for Approximate Computing
Written by: Sara A. Metwalli
For Hara Lab in Tokyo Institute of Technology


#### This is v1.0 of SSA

Install SSA
-------------
1. Download and install KLEE from here.
For more information on KLEE and how it’s used, please visit this page.
2. Download SSA files and put it in the same directory as the files to be analyzed.

Before starting:
----------------
1.  KLEE only handles fixed-point operations, so, if the application has operations with non-fixed-point operators, the user needs to convert these operations into fixed-point first before inputting it to the tool.

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
