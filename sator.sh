
parfile=$1

make

python main.py $parfile > /dev/null 2>&1 &
