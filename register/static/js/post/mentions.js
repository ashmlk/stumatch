$(document).ready(function () {
	var tribute = new Tribute({
		values: function (text, cb) {
			getUsernames(text, users => cb(users));
		},
		lookup: 'username',
		fillAttr: 'username',
		selectClass: 'tributehighlight',
		noMatchTemplate: function () {
			return '<span style:"visibility: hidden;"></span>';
		},
		menuItemTemplate: function (item) {
			return '<div class="p-1"><div class="d-flex"><div class="mx-1 mr-2">' +
					'<img class="rounded-circle" height="30px" width="30px" src="' + item.original.image + '"/>' +
					'</div><div class="name mx-1"><div class="h6">' + item.original.username +  
					'</div><div class="text-primary small">' +  + '</div></div></div></div>'
		},
		selectTemplate: function (item) {
			return '@' + item.original.username ;
		},
	});

	var tributeHashTag = new Tribute({
		trigger: '#',
		values: function (text, cb) {
			getHashtags(text, tags => cb(tags));
		},	
		lookup: 'name',
		fillAttr: 'name',
		selectClass: 'tributehighlight',
		noMatchTemplate: function () {
			return '<span style:"visibility: hidden;"></span>';
		},
		menuItemTemplate: function (item) {
			return '<div class="p-2"><div class="d-flex"><div class="name mx-1"><div class="h6">#' + item.original.name + '</div></div></div></div>'
		},
		selectTemplate: function (item) {
			return '#' + item.original.name ;
		},
	});
	tributeHashTag.attach(document.getElementById("id_content"));
	tribute.attach(document.getElementById("id_content"));
	

	function getUsernames(text, cb){
		var xhr = new XMLHttpRequest();
		xhr.open('GET', '/get/user/mentions?q='+text, true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onload = function () {
			var data = JSON.parse(xhr.responseText);		
			if (xhr.readyState === 4 && xhr.status == "200") {
				cb(data);
			} else if (xhr.status === 403) {
				cb([]);
			}
		}
		xhr.send(null);
	}

	function getHashtags(text, cb){
		var xhr = new XMLHttpRequest();
		xhr.open('GET', '/taggit/?query='+text, true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onload = function () {
			var data = JSON.parse(xhr.responseText);		
			if (xhr.readyState === 4 && xhr.status == "200") {
				cb(data);
			} else if (xhr.status === 403) {
				cb([]);
			}
		}
		xhr.send(null);
	}

	$('#id_content').highlightWithinTextarea({
		highlight: /\B@(?<!@@)(\w{1,31})/gi
	});
	$('#id_content').highlightWithinTextarea({
		highlight: /\B#(?<!##)(\w)/gi
	});
})