$(document).ready(function() {
	$("#id_subject").keyup(function() {
		var search = $("#id_subject").val();
		if (search.length > 0) {
			$.ajax({type: "POST",
				url: "suggest/",
				data: "search=" + search,
				success: function(message) {
					$("#suggestion").empty();
					if (message.length > 0) {
						message = "Do you mean: " + message + "?";
						$("#suggestion").append(message);
					}
				}
			});
		} else {
			// Empty suggestion list
			$("#suggestion").empty();
		}
	});
});

!function(d,s,id)
	{var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
	if(!d.getElementById(id))
			{js=d.createElement(s);
			js.id=id;js.src=p+"://platform.twitter.com/widgets.js";
			fjs.parentNode.insertBefore(js,fjs);}}
			(document,"script","twitter-wjs");

function sort(){
	var sortid = $('sortid').val();
	$.ajax({
		type: "POST",
		url: "/codeprep/sort/",
		data: { sortid: sortid },
	}).done(function(data){
		$('list-group').html(data.html);
	});
}
