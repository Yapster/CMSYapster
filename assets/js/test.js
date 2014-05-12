$(document).ready(function(){
	$('#form .seperator').height($("#form").height());
	function calculate(){
		var space = ($("#form").width() - 2 * 500)/3 - 1;
		if(space < 0){
			space = 15;
			$('#form').css("padding-bottom","15px");
		}
		else{
			$('#form').css("padding-bottom","0");
		}
		$('.group').css("margin-left",space + "px");
	}
	calculate();
	$(window).resize(function(){
		calculate();
	});
});