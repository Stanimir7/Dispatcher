<!DOCTYPE html>
<html>
<head>
<title>Dispatcher Driver Registration</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet" href="/css/w3.css">

</head>
<body>
<?php
if (isset($_POST['Submit']))
{
    #ini_set('display_errors',1);
    #error_reporting(E_ALL);
    
    //API Url
    #$url = $_SERVER['HTTP_HOST'].'/dispatcher/register_driver';
    $url = 'localhost/dispatcher/register_driver';
    #echo $url;
    
    //Initiate cURL.
    $ch = curl_init($url);
     
    //The JSON data.
    $jsonData = array(
        'first_name' => $_POST['first_name'],
        'last_name' => $_POST['last_name'],
        'phone_number' => $_POST['phone_number']
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
     
    //Execute the request
    $result = json_decode(curl_exec($ch));
    if (isset($result)) {
        if ($result->{"status"} == "success")
            echo "Success.";
        else {
            if ($result->status == 'error') #could be 'info' or something
                echo "<h3>Error: ".$result->status."</h3>";
            echo "<p>Message: ".$result->message."</p>";
            #var_dump($result);
        }
    } else
        echo "Empty response. Panic.";
    #if(curl_errno($ch))
    #    echo curl_error($ch);
} else {
?>
    <br>
    <div class="w3-container">
        <div class="w3-card-4">
            <div class="w3-container w3-green">
                <h2>Dispatcher Driver Registration</h2>
            </div>
            <form id='signup' method='post'
                accept-charset='UTF-8' class="w3-container">
                
                <input type='hidden' name='submitted' id='submitted' value='1'/>
                <label for='first_name' >First Name*: </label>
                    <input type='text' name='first_name' id='first_name' maxlength="50" class="w3-input w3-border" />
                <label for='last_name' >Last Name*:</label>
                    <input type='text' name='last_name' id='last_name' maxlength="50" class="w3-input w3-border" />
                <label for='phone_number' >Phone Number*:</label>
                    <input type='text' name='phone_number' id='phone_number' maxlength="50" class="w3-input w3-border" />
       
                <span class="w3-container"><input type='submit' name='Submit' value='Submit' class="w3-btn w3-blue" /></span>
                    
            </form>
        </div>
    </div>
<?php
}
?>

</body>
</html>
