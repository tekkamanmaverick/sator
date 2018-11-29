
if [[ $# -lt 1 ]]; then
    echo No parameter file specified! Exiting...
    exit
fi

make

python main.py $1 > /dev/null 2>&1 &
