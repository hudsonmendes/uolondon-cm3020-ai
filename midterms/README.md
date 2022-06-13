# Genetic Algorithm

## Introduction

## Experiments

### "Atavism Threshold" at 0.5

#### 5 genes
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 5 \
        --target_folder "./evolution/experiment_atavism-050_gene-05_pop-010_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 5 \
        --target_folder "./evolution/experiment_atavism-050_gene-05_pop-010_epoch-100"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 5 \
        --target_folder "./evolution/experiment_atavism-050_gene-05_pop-100_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 5 \
        --target_folder "./evolution/experiment_atavism-050_gene-05_pop-100_epoch-100"
```

#### 10 genes
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 10 \
        --target_folder "./evolution/experiment_atavism-050_gene-10_pop-010_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 10 \
        --target_folder "./evolution/experiment_atavism-050_gene-10_pop-010_epoch-100"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 10 \
        --target_folder "./evolution/experiment_atavism-050_gene-10_pop-100_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 10 \
        --target_folder "./evolution/experiment_atavism-050_gene-10_pop-100_epoch-100"
```

#### 15 genes
```
python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 15 \
        --target_folder "./evolution/experiment_atavism-050_gene-15_pop-010_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 10 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 15 \
        --target_folder "./evolution/experiment_atavism-050_gene-15_pop-010_epoch-100"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 10 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 15 \
        --target_folder "./evolution/experiment_atavism-050_gene-15_pop-100_epoch-010"

python cli.py evolution optimise \
        --genesis_filepath "/Users/hudsonmendes/Workspaces/hudsonmendes-estudos/cm3020-ai/midterms/evolution/genesis.evo" \
        --n_generations 100 \
		--hp_pop_size 100 \
		--hp_exp_threshold=0.2 \
        --hp_gene-count 15 \
        --target_folder "./evolution/experiment_atavism-050_gene-15_pop-100_epoch-100"
```