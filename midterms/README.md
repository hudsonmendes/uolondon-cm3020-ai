# Genetic Algorithm

## Introduction

## Experiments

### Atavism at 0%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.10/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.10/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.10/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```

### Atavism at 10%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.10/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.10/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.10/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```

### Atavism at 20%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.10/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.10/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.10/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.1 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```

### Atavism at 0%, Point Mutation Rate at 25%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.25/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.25/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.00/pmr=0.25/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.0 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```
### Atavism at 10%, Point Mutation Rate at 25%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.25/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.25/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.10/pmr=0.25/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.1 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```
### Atavism at 20%, Point Mutation Rate at 25%
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.25/genes=05" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 5

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.25/genes=10" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 10

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.gen" \
        --target_folder "evolution/atavism=0.20/pmr=0.25/genes=15" \
        --n_generations 250 \
        --crossover_min_len 0.25 \
        --crossover_max_len 0.75 \
        --point_mutation_rate 0.2 \
        --point_mutation_amount -0.15 \
        --shrink_mutation_rate 0.1 \
        --grow_mutation_rate 0.25 \
        --expression_threshold 0.2 \
        --population_size 100 \
        --simulation_steps 2400 \
        --gene_count 20
```