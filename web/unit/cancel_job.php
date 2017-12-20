<?php

  ini_set('display_errors',1);
  error_reporting(E_ALL);

  $url = 'localhost/dispatcher/cancel_job';
  
  //Initiate cURL
  $ch = curl_init($url);
  
  //JSON Data
  $jsonData = array(
  'job_id' => '1'
  );
  //Encode the array into JSON.
  $jsonDataEncoded = json_encode($jsonData);
  
  //Tell cURL that we want to send a POST request.
  curl_setopt($ch, CURLOPT_POST, 1);
     
  //Attach our encoded JSON string to the POST fields.
  curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonDataEncoded);
 // curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  
  //Set the content type to application/json
  curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
  // die('here');
	

  if(curl_exec($ch) === true) {
  echo '\nDone';	
  } else {
  echo curl_error($ch);
  }
  curl_close($ch);
  ?>
