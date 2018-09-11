#!/bin/bash

# while screen exists

# specify screen of interest
test_screen=t7_eval_3

# initialize screen existence value
var=$(screen -S ${test_screen} -X select .; echo $?)

# evaluate if screen exists every 
while [ "${var}" == "0" ]
do
	echo "Process ${test_screen} still running.  Waiting another 10 minutes..."
	sleep 600
	var=$(screen -S ${test_screen} -X select .; echo $?)
done

# run other script
./train_all2.sh
