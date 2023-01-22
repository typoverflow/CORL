all_args=("$@")
task=$1
quality=$2
rest_args=("${all_args[@]:2}")

source scripts/config.sh
project="D2MG-transfer"

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

for algo in "td3_bc" "cql" "iql"; do
for t in ${tasks[@]}; do
    for q in ${qualities[@]}; do
        echo python3 test_bench/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml ${rest_args[@]} 
        python3 test_bench/$algo.py --config_path=configs/$algo/$t/${q/'-'/'_'}_v2.yaml ${rest_args[@]} 
    done
done
done
