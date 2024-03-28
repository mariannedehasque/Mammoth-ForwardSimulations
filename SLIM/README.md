# SLiM script to simulate a bottleneck and recovery in a WF population
Written by Hernán E. Morales - hernan.moral [at] gmail [dot] com

### The simulation is done in three steps. Here a short example with a small population (Ne=1000) and a short chromosome (10Mb)

-- dependencies:
msprime 1.0.1
pyslim 0.600
tskit 0.3.6
allel 1.3.5
slim 3.6


1) Step one - burn in simulation with msprime

```python mammoth_wrangler_step1_22_11_22.py --recRate 1e-7 --Ne 1000 --muRate 1.2e-8 --chromLen 1e7 --outPath ./ --seed 12345678 --outName out_mammoth_test```

2) Convert tree sequence recording output into slim file

```slim -d "chrSize=1e7" -d "treeIN='./out_mammoth_test_Ne1000.0_mu1.2e-8_rho1e-7_seLen10000001.0_seed12345678.tree'" mammoth_wrangler_step2_22_11_22_tree2full.slim```

3) Bottleneck simulation

```slim -d "DIR='./'" -d "slimIN='./out_mammoth_test_Ne1000.0_mu1.2e-8_rho1e-7_seLen10000001.0_seed12345678_fullOut.slim'" mammoth_wrangler_step3_22_11_22_btlnck.slim```

* see the script for all the parameters that can be varied by using -d "param=value"
