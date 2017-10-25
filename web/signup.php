<form id='signup' action='/dispatcher/register_driver' method='post'
2
    accept-charset='UTF-8'>
3
<fieldset >
4
<legend>Register</legend>
5
<input type='hidden' name='submitted' id='submitted' value='1'/>
6
<label for='first_name' >Your First Name*: </label>
7
<input type='text' name='first_name' id='first_name' maxlength="50" />
8
<label for='last_name' >Email Address*:</label>
9
<input type='text' name='email' id='email' maxlength="50" />
10
 
11
<label for='username' >UserName*:</label>
12
<input type='text' name='username' id='username' maxlength="50" />
13
 
14
<label for='password' >Password*:</label>
15
<input type='password' name='password' id='password' maxlength="50" />
16
<input type='submit' name='Submit' value='Submit' />
17
 
18
</fieldset>
19
</form>


<?php

?>