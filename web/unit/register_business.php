
<?php
//API Url
    #$url = $_SERVER['HTTP_HOST'].'/dispatcher/register_driver';
    $url = 'localhost/dispatcher/register_business';
    #echo $url;
    
    //Initiate cURL.
    $ch = curl_init($url);
     
    //The JSON data.
    $jsonData = array(
    'merch_id' => '99',
    'merch_name'=> 'Unit Test Inc',
    'phone_num'=> '12345',
    'merch_address'=> '123 lane'
    );
    #echo $_POST['first_name'];
    #echo $_POST['last_name'];
    #echo $_POST['phone_number'];
    #var_dump($jsonData);
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