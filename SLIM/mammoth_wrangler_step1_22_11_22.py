# -*- coding: utf-8 -*-
"""
Script to generate a burn in population in mutation-drift equilibrium with msprime
Written by Hernán E. Morales - hernan.moral [at] gmail.com
"""
import msprime, pyslim, tskit
import argparse
import allel
import datetime

print(msprime.__version__)
print(pyslim.__version__)
print(tskit.__version__)
print(allel.__version__)

#### Get arguments
parser = argparse.ArgumentParser()
# tree name
parser.add_argument('--recRate',nargs='+',type=str)
# Ne for recapitation
parser.add_argument('--Ne',nargs='+',type=str)
# recombination rates file
parser.add_argument('--muRate',nargs='+',type=str)
# chrom len
parser.add_argument('--chromLen',nargs='+',type=str)
# outPath
parser.add_argument('--outPath',nargs='+',type=str)
# seed
parser.add_argument('--seed',nargs='+',type=int)
# outName
parser.add_argument('--outName',nargs='+',type=str)


args = parser.parse_args()
recRate=str(args.recRate[0])
Ne=float(args.Ne[0])
muRate=str(args.muRate[0])
chromLen=float(args.chromLen[0])+1
outPath=str(args.outPath[0])
outName=str(args.outName[0])
seed=int(args.seed[0])

# =============================================================================
# Ne=1000
# muRate=1.2e-8
# recRate=1e-8
# seed=1234
# chromLen=10e6+1
# outPath="./"
# outName="out_mammoth_burnin_test"
# =============================================================================

print("start demog_model")
e = datetime.datetime.now()
print ("Current date and time = %s" % e)

demog_model = msprime.Demography()
demog_model.add_population(initial_size=Ne)

print("start sim_ancestry")
e = datetime.datetime.now()
print ("Current date and time = %s" % e)

ots = msprime.sim_ancestry(
        samples=Ne,
        sequence_length=chromLen,
        demography=demog_model,
        random_seed=seed,
        recombination_rate=recRate)

print("start annotate_defaults")
e = datetime.datetime.now()
print ("Current date and time = %s" % e)

ots = pyslim.annotate_defaults(ots, model_type="WF", slim_generation=1)


# use a large slim_generation to avoid having mutations with negative time values
GENS=int(Ne*100)
mut_model = msprime.SLiMMutationModel(type=1,slim_generation=GENS,next_id=1)              

print("start sim_mutations")
e = datetime.datetime.now()
print ("Current date and time = %s" % e)


ots = msprime.sim_mutations(
            ots,
            rate=muRate,
            model=mut_model,
            keep=True, 
            random_seed=seed)
print(f"The ots sequence has {ots.num_trees} trees on a genome of length {ots.sequence_length},"
      f" {ots.num_individuals} individuals, {ots.num_samples} 'sample' genomes,"
      f" and {ots.num_mutations} mutationsat "
      f"{ots.num_sites} distinct sites.")

pi_diver=float(ots.diversity())
print("pi="+str(pi_diver))


print("start dump tree")

FILEname=str(outPath)+"/"+str(outName)+"_Ne"+str(Ne)+"_mu"+str(muRate)+"_rho"+str(recRate)+"_seLen"+str(chromLen)+"_seed"+str(seed)+".tree" 
print('Output '+FILEname)
ots.dump(FILEname)
print("finished dump tree")
