<?php
header("Content-Type: text/html; charset=UTF-8");
// 로그인 체크 모듈
@include_once("m.cklogin.inc.php");



	$clinic_id = $_GET['no'];
	

?>

<script language="javascript">

function openWinTopDel(clinic_id, image){  
	//image = decodeURIComponent(image) ;
    window.open("clinic.info.top.delete.php?no="+clinic_id+"&image="+image, "탑이미지 삭제", "width=800, height=600, toolbar=no, menubar=no, scrollbars=no, resizable=yes" );  

}


function openWinGalDel(clinic_id, order_n, image){  
	//image = decodeURIComponent(image) ;
    window.open("clinic.gallery.delete.php?no="+clinic_id+"&order_n="+order_n+"&image="+image, "갤러리 삭제", "width=800, height=600, toolbar=no, menubar=no, scrollbars=no, resizable=yes" );  

}
function openWinIntroDel(clinic_id, order_n, image){  
	//image = decodeURIComponent(image) ;
    window.open("clinic.intro.delete.php?no="+clinic_id+"&order_n="+order_n+"&image="+image, "병원소개 삭제", "width=800, height=600, toolbar=no, menubar=no, scrollbars=no, resizable=yes" );  

}

function openWinSubDel(clinic_id, order_n, image, i){  
	//image = decodeURIComponent(image) ;
    window.open("clinic.subject.delete.php?no="+clinic_id+"&order_n="+order_n+"&image="+image+"&i="+i, "진료과목 삭제", "width=800, height=600, toolbar=no, menubar=no, scrollbars=no, resizable=yes" );  

}

function openWinHelpDel(clinic_id, order_n, image){  
	//image = decodeURIComponent(image) ;
    window.open("clinic.help.delete.php?no="+clinic_id+"&order_n="+order_n+"&image="+image, "진료안내 삭제", "width=800, height=600, toolbar=no, menubar=no, scrollbars=no, resizable=yes" );  

}
</script>


<html>
<body topmargin="0" leftmargin="0">

<div id="skip" style=" position:fixed; top:0;  left: 0px; width:100%; background-Color:#ffffff"> 
 <ul>
  <ui><a href="#info"> ★병원 정보 </a></ui>
  <ui><a href="#gallery"> ★병원 갤러리  </a></ui>
  <ui><a href="#intro"> ★병원 소개  </a></ui>
  <ui><a href="#subject"> ★진료 과목  </a></ui>
  <ui><a href="#help"> ★진료 안내  </a></ui>
 </div>

 <div style="margin-top: 50px; ">




<?php

		require_once("m.dbcon.php");
		mysql_query("set autocommit=0;");
		mysql_query("begin;");


		$query2 = "SELECT * FROM clinic WHERE clinic_id = '$clinic_id' ";
		$result2 = mysql_query($query2);
		if (mysql_error()) {
			mysql_query("rollback;");
			mysql_close($connect_db);	
			die( "mysql error 33: ".mysql_error() ); 
		}
		while($row = mysql_fetch_assoc($result2)) {
		     $clinic_id = $row['clinic_id'];
		     $clinic_address = $row['address'];
		     $clinic_logo_string = $row['clinic_logo_string'];
		     $clinic_tel = $row['tel'];
		     $clinic_name = $row['clinic_name'];
		     $clinic_top_image = $row['clinic_top_image'];
		}

	?>



<div id ="info" style="width:100%; float:left; background-Color:#FFFF2F">

	<h2> 병원 정보 </h2>

	<form action='clinic.info.update.php' method='POST' enctype='multipart/form-data'>
		
		병원 ID : <?=$clinic_id?>  
		 <input type='hidden' name='clinic_id' value="<?=$clinic_id?>"  > <br>



	<?php
		if($clinic_top_image) echo "<image src='../image_home/$clinic_top_image' width='200'><br>"; ?>
	탑 이미지 : <input type='file' name='clinic_top_image'>
	<a href='#' onClick="openWinTopDel(<?=$clinic_id?>, '<?=$clinic_top_image?>');">삭제</a><br><br>


	<font color=red>*</font>
	병원 이름 : 
	<input type='text' name='clinic_name' value="<?=$clinic_name?>"><br>

	병원 전화번호 : 
	<input type='text' name='tel' value=<?=$clinic_tel?>><br>
	병원 주소 ::
	<input type='text' name='address' value="<?=$clinic_address?>"><br>
	상세 정보  :
	<input type='text' name='clinic_info' value="<?=$clinic_logo_string?>"><br>

	<input type='reset'> <input type='submit'> <br>
	</form>


</div>


<div id='gallery'  style="float:left;width:50%; background-Color:#F2FFFF">


	


	<h2> 병원 갤러리 </h2>

	<form action='clinic.gallery.update.php' method='POST' enctype='multipart/form-data'>
		<input type='hidden' name='clinic_id' value="<?=$clinic_id?>"  > 

			<br>

			<?php
				$query2 = "SELECT * FROM clinic_gallery WHERE clinic_id = '$clinic_id' ";
				$result2 = mysql_query($query2);
				if (mysql_error()) {
					mysql_query("rollback;");
					mysql_close($connect_db);	
					die( "mysql error 33: ".mysql_error() ); 
				}

				$order_n =0;

				$imageArray = array();
				while($row = mysql_fetch_assoc($result2)) {
				       

				     $order_n = $row['order_n'];
				     $imageArray[$order_n] = $row['image'];


				}

				for($i=0; $i<20; $i++){

					if(!empty($imageArray[$i])){
						echo "<image src='../image_home/$imageArray[$i]' width='200'>";
						echo "<a href='#' onClick='openWinGalDel($clinic_id, $i, \"$imageArray[$i]\");'>삭제</a><br>";
					}

					 echo "갤러리 이미지 ".$i." : <input type='file' name='profileimgfile[$i]'><br>";
					
				}


			?>

			<br>
		<input type='reset'> <input type='submit'> <br>
	</form>

</div>
<div id="intro" style="float:right;width:50%; background-Color:#FFF2FF">

	<h2> 병원 소개 </h2>



	<form action='clinic.intro.update.php' method='POST' enctype='multipart/form-data'>
	<input type='hidden' name='clinic_id' value="<?=$clinic_id?>"  > 

	<br>



		<?php
			$query2 = "SELECT * FROM clinic_intro WHERE clinic_id = '$clinic_id' ";
			$result2 = mysql_query($query2);
			if (mysql_error()) {
				mysql_query("rollback;");
				mysql_close($connect_db);	
				die( "mysql error 33: ".mysql_error() ); 
			}

			$order_n =0;

			$imageArray = array();
			while($row = mysql_fetch_assoc($result2)) {
			       

			     $order_n = $row['order_n'];
			     $imageArray[$order_n] = $row['image'];


			}

			for($i=0; $i<20; $i++){

				if(!empty($imageArray[$i])){
					echo "<image src='../image_intro/$imageArray[$i]' width='200'>";
					echo "<a href='#' onClick='openWinIntroDel($clinic_id, $i, \"$imageArray[$i]\");'>삭제</a><br>";
				}

				 echo "소개 이미지 ".$i." : <input type='file' name='profileimgfile[$i]'><br>";
				
			}


		?>




	<br>
	<input type='reset'> <input type='submit'> <br>
	</form>
	



</div>
<div id="subject" style="clear:both;width:50%; float:left;  background-Color:#FFFFF2">

	<h2> 병원 진료 과목  </h2>

	<form action='clinic.subject.update.php' method='POST' enctype='multipart/form-data'>
		<input type='hidden' name='clinic_id' value="<?=$clinic_id?>"  > <br>



			
	


		<?php
			$query2 = "SELECT * FROM clinic_subject WHERE clinic_id = '$clinic_id' ";
			$result2 = mysql_query($query2);
			if (mysql_error()) {
				mysql_query("rollback;");
				mysql_close($connect_db);	
				die( "mysql error 33: ".mysql_error() ); 
			}


			$LogoImage = array();
			$ImageAraay1 = array();
			$ImageAraay2 = array();
			$ImageAraay3 = array();
			$ImageAraay4 = array();
			$ImageAraay5 = array();

			while($row = mysql_fetch_assoc($result2)) {
			       

			     $order_n = $row['order_n'];
			     $LogoImage[$order_n] = $row['image_0'];
				 $ImageAraay1[$order_n] = $row['image_1'];
				 $ImageAraay2[$order_n] = $row['image_2'];
				 $ImageAraay3[$order_n] = $row['image_3'];
			     $ImageAraay4[$order_n] = $row['image_4'];
			     $ImageAraay5[$order_n] = $row['image_5'];


			}

			for($i=0; $i<10; $i++){

				echo "진료과목".$i."<br>";

				if(!empty($LogoImage[$i])){
					echo "<image src='../image_subject/$LogoImage[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$LogoImage[$i]\", 0);'>삭제</a><br>";
				}

				echo "대표이미지 : <input type='file' name='LogoImage[$i]'><br>";




				if(!empty($ImageAraay1[$i])){
					echo "<image src='../image_subject/$ImageAraay1[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$ImageAraay1[$i]\", 1);'>삭제</a><br>";
				}
				
				echo "이미지1 : <input type='file' name='ImageAraay1[$i]'><br>";

				if(!empty($ImageAraay2[$i])){
					echo "<image src='../image_subject/$ImageAraay2[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$ImageAraay2[$i]\", 2);'>삭제</a><br>";
				}
				
				echo "이미지2 : <input type='file' name='ImageAraay2[$i]'><br>";

				if(!empty($ImageAraay3[$i])){
					echo "<image src='../image_subject/$ImageAraay3[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$ImageAraay3[$i]\", 3);'>삭제</a><br>";
				}
				
				echo "이미지3 : <input type='file' name='ImageAraay3[$i]'><br>";

				if(!empty($ImageAraay4[$i])){
					echo "<image src='../image_subject/$ImageAraay4[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$ImageAraay4[$i]\", 4);'>삭제</a><br>";
				}
				
				echo "이미지4 : <input type='file' name='ImageAraay4[$i]'><br>";

				if(!empty($ImageAraay5[$i])){
					echo "<image src='../image_subject/$ImageAraay5[$i]' width='200'>";
				   	echo "<a href='#' onClick='openWinSubDel($clinic_id, $order_n, \"$ImageAraay5[$i]\", 5);'>삭제</a><br>";
				}
				
				echo "이미지5 : <input type='file' name='ImageAraay5[$i]'><br><br>";
				
			}


		?>

		<br> <br><br>
		<input type='reset'> <input type='submit'> <br><br>
	</form>





	
</div>
<div id="help" style=" float:right; width:50%;background-Color:#EFEFEF">

<h2> 병원 진료안내 </h2>

<form action='clinic.help.update.php' method='POST' enctype='multipart/form-data'>
		<input type='hidden' name='clinic_id' value="<?=$clinic_id?>"  > 




	<br>
	<br>

		<?php
			$query2 = "SELECT * FROM clinic_help WHERE clinic_id = '$clinic_id' ";
			$result2 = mysql_query($query2);
			if (mysql_error()) {
				mysql_query("rollback;");
				mysql_close($connect_db);	
				die( "mysql error 33: ".mysql_error() ); 
			}

			$order_n =0;

			$imageArray = array();
			while($row = mysql_fetch_assoc($result2)) {
			       

			     $order_n = $row['order_n'];
			     $imageArray[$order_n] = $row['image'];


			}

			for($i=0; $i<20; $i++){

				if(!empty($imageArray[$i])){
					echo "<image src='../image_help/$imageArray[$i]' width='200'>";
					echo "<a href='#' onClick='openWinHelpDel($clinic_id, $i, \"$imageArray[$i]\");'>삭제</a><br>";
				}

				 echo "안내 이미지 ".$i." : <input type='file' name='profileimgfile[$i]'><br>";
				
			}


		?>


	<br>
	<input type='reset'> <input type='submit'> <br>
	</form>

</div>

 </div>


</body>
</html>
