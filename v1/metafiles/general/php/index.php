
<?php

include "../../general/php/tools.php";

$html = file_get_contents("../../general/html/template.html");
$html = fromJson("../json/structure.json", $html);
$html = fromJson("../../general/json/structure.json", $html);
echo $html;

?>
