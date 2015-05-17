<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="600">
</head>
<body>

<table border=1>
<tr>
  <th><h2>Points</h2></th>
  <th><h2>Weather</h2></th>
<tr>
<tr>
<td>
<h3>The Allowance/Point Totals are as follows:</h3>

<?php
$AttributeLkup = array( 0 =>'none', 1 => 'all', 2 => 'points', 3 => 'allowance' );
$NameLkup = array( 0 => 'none', 1 => 'Child1', 2 => 'Child2', 3 => 'Child3');

if(($csvfile = fopen("/home/root/scripts/database.txt", "r")) !== FALSE) {
  while (($data = fgetcsv($csvfile, 1000, ",")) !== FALSE) {
    $num = count($data);
    $row++;
    if($data[1] == 2) {
      echo $NameLkup[$data[0]] . " has " . $data[2] . " " . $AttributeLkup[$data[1]] . "<br />\n";
    } else {
      echo $NameLkup[$data[0]] . " has $" . $data[2] . " saved in " . $AttributeLkup[$data[1]] . "<br />\n<br />\n";
    }
//    for ($c=0; $c < $num; $c++) {
//      echo $data[$c] . "<br />\n";
//    }
  }
}

echo "<br />Command string is: <b>name attribute <i>value</i></b><br />\n";
echo "Valid names are: <b>child3|c3</b>, <b>child2|c2</b>, <b>child3|c3</b><br />\n";
echo "Valid attributes are: <b>points|pnt|pnts</b>, <b>allowance|alw</b><br />\n";
echo "Value is a <b>positive or negative number</b> depending on how much you want to add or take away from the specified attribute.<br />\n"
?>
</td>
<td>
<iframe src="http://mobile.weather.gov/index.php?lat=33.07&lon=-96.07" height="500">
</td>
</tr>
</table>
</body>
</html>

