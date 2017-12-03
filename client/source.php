<?php
	exec('python3.4 cgi-bin/kde.py', $dataFromPython);
	#echo($dataFromPython);
	echo(empty($dataFromPython)) ? "python não carregou" : json_encode($dataFromPython);
?>