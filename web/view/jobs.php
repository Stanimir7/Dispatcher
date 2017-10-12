<html>
<body>
<?php
$mysqli = new mysqli("localhost", "dispatcher", "dispatcher", "dispatcher");

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}
echo $mysqli->host_info . "\n";

$res = $mysqli->query("SELECT * FROM Job");
//while ($row = $res->fetch_assoc()) {
//	echo $row;
//}
echo '<table>';
while ($row = $res->fetch_assoc()) {
    echo '<tr>';
    foreach($row as $field) {
        echo '<td>' . htmlspecialchars($field) . '</td>';
    }
    echo '</tr>';
}
echo '</table>';
echo 'EOF';
?>

</html>
</body>
