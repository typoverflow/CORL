all_args=("$@")
task=$1
quality=$2
seed=$3
rest_args=("${all_args[@]:3}")

source scripts/config.sh
project="IQL-"$phase

if [ $task == "all" ]; then
    tasks=( "halfcheetah" "hopper" "walker2d")
else
    tasks=( $task )
fi

if [ $quality == "all" ]; then
    qualities=( "medium" "medium-replay" "medium-expert" "random" )
else
    qualities=( $quality )
fi

for t in ${tasks[@]}; do
    for q in ${qualities[@]}; do
        echo python3 algorithms/iql.py --config_path=configs/iql/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]} 
        python3 algorithms/iql.py --config_path=configs/iql/$t/${q/'-'/'_'}_v2.yaml --seed $seed --project $project --entity $entity ${rest_args[@]} 
    done
done
