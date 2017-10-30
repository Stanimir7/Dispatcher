<!DOCTYPE html>
<html>
<head>
<title>Dispatcher Driver Deregistration</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet" href="/css/w3.css">

</head>
<body>
    <br>
    <div class="w3-container">
        <div class="w3-card-4">
            <div class="w3-container w3-blue">
                <h2>Dispatcher Driver Deregistration</h2>
            </div>
<?php
if (isset($_POST['Submit']))
{
    echo '<div class="w3-container">';
    #ini_set('display_errors',1);
    #error_reporting(E_ALL);
    
    //API Url
    #$url = $_SERVER['HTTP_HOST'].'/dispatcher/register_driver';
    $url = 'localhost/dispatcher/confirm_code';
    #echo $url;
    
    //Initiate cURL.
    $ch = curl_init($url);
     
    //The JSON data.
    $jsonData = array(
        'phone_number' => $_POST['phone_number']
    );
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
        if (empty($result->status)){
			//var_dump($result);
			//The "Conf Code" form
			//TODO: possibly do a pre-check before forwarding browser to flask endpoint
			?>
			<p>A code has been sent to the phone number, enter the confirmation code below.</p>
			<form id='conf_form' action='/dispatcher/deregister_driver' method='post' accept-charset='UTF-8' class="w3-container">
				<input type='hidden' name='key' id='key' value="<?php echo $result->key; ?>"/>
                <label for='conf_code' >Confirmation Code*:</label>
                    <input type='text' name='conf_code' id='conf_code' maxlength="50" class="w3-input w3-border" />
       
                <span class="w3-container"><input type='submit' name='Submit' value='Submit' class="w3-btn w3-blue" /></span>
                    
            </form>
			
		   
		   <?php
        }
        else {
            echo "<h3>Error</h3>";
            echo "<p>".$result->message."</p>";
            var_dump($result);
        }
    } else
        echo "Empty response. Panic.";
    #if(curl_errno($ch))
    #    echo curl_error($ch);
     #echo '<span class="w3-container"><a href="deregister.php" class="w3-btn w3-blue">Go Back</a></span>';
    echo '</div>';
} else {
?>
    
            <form id='phone_form' method='post'
                accept-charset='UTF-8' class="w3-container">
                <label for='phone_number' >Phone Number*:</label>
                    <input type='text' name='phone_number' id='phone_number' maxlength="50" class="w3-input w3-border" />
       
                <span class="w3-container"><input type='submit' name='Submit' value='Submit' class="w3-btn w3-blue" /></span>
                    
            </form>

<?php
}
?>
        </div>
    </div>
</body>
</html>
