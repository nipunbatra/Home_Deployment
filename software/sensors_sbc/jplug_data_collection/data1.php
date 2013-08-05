<?php

if(isset($_REQUEST['macaddress']))
{

    $Macaddress=$_REQUEST['macaddress'];
    
}

if(isset($_REQUEST['datapoint']))
{
    
	$data=$_REQUEST['datapoint'];
    
}
else
{
	$data="";
}

date_default_timezone_set('Asia/Kolkata');

if(strlen(trim($data))>1)
{

	$data=$data;
	
	//$file = fopen(sprintf('"/home/nipun/Desktop/%s"',$Macaddress), "a");
	$file = fopen("/home/nipun/Desktop/alpha", "a");
	fwrite($file,$data);
	fclose($file);
	//$r = new HttpRequest('http://localhost:9005', HttpRequest::METH_POST);
	//$r->addPostFields(array('user' => 'mike', 'pass' => 's3c|r3t'));
	//$r->send();
    	echo "File accepted"."\r\n";
}
else
{
	echo "NO INPUT"."<br/><br/>";
}


?>


