#!/bin/bash

flag=$1
function_dialog(){
if [ "$flag" = "name" ]; then
	read -p "Введите, фамилию и имя через пробел: " name
	echo "$name"
	exit
fi

if [ $flag = 'praise' ]; then
	while :
	do
        	read -p "Добавить похвалу учителя? y/n: " q
		if [[ "$q" = "y" ]]; then
        		echo "y"
        		exit
		elif [[ "$q" = "n" ]]; then
        		echo "n"
        		exit
		fi
	done
fi
}
return=$(function_dialog)
echo $return

