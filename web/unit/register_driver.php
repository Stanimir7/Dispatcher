<?php

ini_set('display_errors',1);
error_reporting(E_ALL);

//API Url
#$url = $_SERVER['HTTP_HOST'].'/dispatcher/register_driver';
$url = 'localhost/dispatcher/register_driver';
#echo $url;

//Initiate cURL.
$ch = curl_init($url);
 
//The JSON data.
$jsonData = array(
    'first_name' => 'Billy',
    'last_name' => 'Jones',
    'phone_number' => '12345'
);
 
//Encode the array into JSON.
$jsonDataEncoded = json_encode($jsonData);
 
//Tell cURL that we want to send a POST request.
curl_setopt($ch, CURLOPT_POST, 1);
 
//Attach our encoded JSON string to the POST fields.
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonDataEncoded);
 
//Set the content type to application/json
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json')); 
 
//Execute the request
$result = curl_exec($ch);
echo curl_error($ch);

?>