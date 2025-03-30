# SpikeFetch

This GitHub repository contains the code and scripts to generate prefetches using SpikeFetch on SPEC and CloudSuite traces. It also generates result files containing performance metrics like IPC (Instructions Per Cycle), LLC Load Accesses, and LLC Prefetch Requests Issued, which can be used to calculate prefetching accuracy and coverage.

## Download datasets

Run the following command to download the SPEC and CloudSuite traces tested in our paper:
```bash
bash download.sh
```
- Ensure you have an active internet connection.
- The traces will be saved to a designated directory (check the script for details).

## Create environment
Set up the required Python environment using Conda:

```bash
conda env create -f environment.yml
```
- This creates an environment named `spikefetch_env` with all necessary dependencies.
- Activate it with:
  ```bash
  conda activate spikefetch_env
  ```

## Building
Compile the SpikeFetch simulator by running:
```bash
./ml_prefetch_sim.py build
```
- This generates the binaries needed for simulation.
- Ensure the environment is activated before running this command.

## Running and Evaluating
Generate prefetch and result files with:
```bash
bash run_spikefetch_trace.sh
```
- **Outputs**:
  - Prefetch files are saved in the `spikefetch_prefetches_traces` folder.
  - Result files (IPC, LLC metrics, etc.) are saved in the `results` folder.
- Use these files to analyze prefetching performance.
