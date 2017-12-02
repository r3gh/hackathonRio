<?php
	//include 'conexao.php';
	
	$params = "";
	// Montagem da query e envio dos dados
	//if(isset($_POST['submitted']) ) {
		$tipoProcessamento = trim($_POST['tipoProcessamento']);
		$pontos = trim($_POST['pontos']);
		
		if($tipoProcessamento=='python'){
			// envia restrição do polígono caso este tenha sido desenhado no mapa
			if(!empty($poligono)) {
				$query = "SELECT ST_X(geom), ST_Y(geom) from alunos_rural WHERE ST_Intersects(geom,ST_Transform(ST_GeomFromText('".$poligono."',3857),4326))".$params.";";
			} 
			else {
				$query = "SELECT ST_X(geom), ST_Y(geom) from alunos_rural WHERE latitude != 0 ".$params.";";
			}

			exec('python cgi-bin/kde.py "'.$query.'"' , $dataFromPython);
			
			echo (empty($dataFromPython)) ? "python não carregou" : json_encode($dataFromPython);
		}
		else if($tipoProcessamento=='php'){
			// envia restrição do polígono caso este tenha sido desenhado no mapa
			if(!empty($poligono)) {
				$query = "SELECT ST_X(geom), ST_Y(geom), bolsista, nascimento, cra, naturalidade, cod_curso, sexo, forma_ingresso, campus, crm from alunos_rural WHERE ST_Intersects(geom,ST_Transform(ST_GeomFromText('".$poligono."',3857),4326))".$params.";";
			} 
			else {
				$query = "SELECT ST_X(geom), ST_Y(geom), bolsista, nascimento, cra, naturalidade, cod_curso, sexo, forma_ingresso, campus, crm from alunos_rural WHERE latitude != 0".$params.";";
			}

			$result = pg_query($query);
			$JSON = json_encode(pg_fetch_all($result));
			
			pg_free_result($result);
			// seta variável de envio como TRUE
			$sent = true;
			print_r($JSON);
		}
	//}
	//print_r($pontos);
	exec('python cgi-bin/kde.py', $dataFromPython);
	
	echo(empty($dataFromPython)) ? "python não carregou" : json_encode($dataFromPython);
?>
