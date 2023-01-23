all_args=("$@")
algo=$1
data_limit=$2
seed=$3
rest_args=("${all_args[@]:3}")

source scripts/config.sh
project="D2MG-DataLimit"

tasks=( "halfcheetah" "hopper")

qualities=( "medium" "random" )

# for algo in "cql" "td3_bc" "iql"; do
for t in ${tasks[@]}; do
    for q in ${qualities[@]}; do
<<<<<<< HEAD
        echo python3 algorithms/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]} --data_limit ${data_limit}
        python3 algorithms/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]} --data_limit ${data_limit}
=======
        echo python3 algorithms/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]}
        python3 algorithms/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]}
>>>>>>> 8e32555f53a3f2ee914ff2b150d711982c1578a5
    done
done
# done
