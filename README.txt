This program requires Python 3.8.0 or later. Run on command line.

Usage: main.py –f TestTrace.trc –s 1024 –b 16 –a 2 –r RR

–f <trace file name> [ name of text file with the trace ]
–s <cache size in KB> [ 1 KB to 8 MB ]
–b <block size> [ 4 bytes to 64 bytes ]
–a <associativity> [ 1, 2, 4, 8, 16 ]
–r <replacement policy> [ RR or RND or LRU for bonus points]

The results will be displayed on the command line and stored in an output file called <tracefile>_output.txt.
