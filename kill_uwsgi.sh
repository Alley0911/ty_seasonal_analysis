#!/bin/bash
uwsgi_id=`ps -ef | grep uwsgi| grep -v grep| awk '{print $2}'`

if [ -z "uwsgi_id" ];then
	echo "not find uwsgi pid"
else
	for id in $uwsgi_id;
		do 	
			kill $id
		done
fi
		
