<?php

  $url = 'localhost/dispatcher/cancel_job';
  
  //Initiate cURL
  $ch = curl_init($url);
  
  //JSON Data
  $jsonData = array(
  'driver_id' => '78',
  'job_id' => '23'
  );
  
  //Encode the array into JSON.
  $jsonDataEncoded = json_encode($jsonData);
  
  //Tell cURL that we want to send a POST request.
  curl_setopt($ch, CURLOPT_POST, 1);
     
  //Attach our encoded JSON string to the POST fields.
  curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonDataEncoded);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  
  //Set the content type to application/json
  curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
	
	echo curl_exec($ch);
	?>
