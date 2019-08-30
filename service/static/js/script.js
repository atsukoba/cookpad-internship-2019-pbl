// add Put/Delete
$.extend({
	"put" : function (url, data, success, error) {
		error = error || function() {};
		return $.ajax({
			"url" : url,
			"data" : data,
			"success" : success,
			"type" : "PUT",
			"cache" : false,
			"error" : error,
			"dataType" : "json"
		});
	},
	"del" : function (url, data, success, error) { 
		error = error || function() {};
		return $.ajax({
			"url" : url,
			"data" : data,
			"success" : success,
			"type" : "DELETE",
			"cache" : false,
			"error" : error,
			"dataType" : "json"
		});
	}
});

// for liked /not liked UI
const liked_svg = '<svg width="45" height="45" viewBox="0 0 45 45" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="22.5" cy="22.5" r="22" fill="#645246" stroke="#645246"/><path d="M34.3289 20.6397L22.4516 32.8142C20.1471 35.1693 16.3984 35.1693 14.095 32.8142C11.7916 30.459 11.7905 26.6248 14.095 24.2685L26.6554 11.4777C28.0381 10.0639 30.2871 10.0639 31.6698 11.4777C33.0514 12.8915 33.0525 15.1899 31.6698 16.6037L21.6161 26.8315C21.1552 27.3027 20.4059 27.3027 19.945 26.8315C19.4841 26.3602 19.4841 25.5941 19.945 25.1228L28.3276 16.6037L26.6554 14.895L18.2727 23.4129C16.8876 24.8292 16.8888 27.1263 18.2727 28.5413C19.6566 29.9563 21.9021 29.9563 23.286 28.5413L33.3397 18.3136C34.4944 17.133 35.0699 15.5874 35.0699 14.0407C35.0699 10.6947 32.4155 8 29.1608 8C27.6481 8 26.1365 8.58969 24.9819 9.77028L12.4227 22.5586C10.8084 24.2117 10 26.3759 10 28.5413C10 33.2093 13.6991 37 18.2727 37C20.3905 37 22.5072 36.1735 24.1227 34.5228L36 22.3483L34.3289 20.6397Z" fill="white"/></svg>'
const like_svg = '<svg width="45" height="45" viewBox="0 0 45 45" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="22.5" cy="22.5" r="22" fill="white" stroke="#645246"/><path d="M18.6302 23.7625L26.6544 15.6089L27.6271 16.6028L19.5886 24.7721L19.5875 24.7732C18.9366 25.4388 18.9366 26.5155 19.5875 27.1811C20.2444 27.8527 21.3161 27.8529 21.9732 27.1814C21.9733 27.1813 21.9734 27.1812 21.9736 27.1811L32.0264 16.9542L32.0273 16.9533C33.6002 15.345 33.5986 12.7362 32.0274 11.1283L32.0273 11.1281C30.4485 9.51388 27.877 9.51379 26.2982 11.1279C26.2981 11.1279 26.298 11.128 26.2979 11.1281L13.7382 23.9181L13.7375 23.9189C11.2429 26.4696 11.2442 30.6144 13.7375 33.1638C16.2371 35.7195 20.3084 35.7193 22.809 33.1639L22.8095 33.1633L34.3294 21.3552L35.301 22.3488L23.7654 34.1731C23.7652 34.1733 23.7651 34.1734 23.7649 34.1736C22.246 35.7253 20.2595 36.5 18.2727 36.5C13.986 36.5 10.5 32.944 10.5 28.5413C10.5 26.5 11.2617 24.4634 12.7799 22.9085C12.7801 22.9083 12.7803 22.9081 12.7804 22.9079L25.3386 10.1206L25.3394 10.1199C26.3974 9.03811 27.7789 8.5 29.1608 8.5C32.1301 8.5 34.5699 10.9614 34.5699 14.0407C34.5699 15.4638 34.0407 16.8815 32.9826 17.9636C32.9825 17.9637 32.9824 17.9638 32.9823 17.964L22.9294 28.1908L22.9285 28.1917C21.7408 29.4062 19.818 29.4062 18.6302 28.1917C17.4364 26.9711 17.4353 24.9849 18.6297 23.7631C18.6298 23.7629 18.63 23.7627 18.6302 23.7625Z" fill="#645246" stroke="#645246"/></svg>'

function doLike(recipe_id) {
    const USERID = "atsuyakoba"
	console.log("request GET to /likes/do, " + USERID + ", " + String(recipe_id))
	res = $.get('/likes/do', {'userid' : USERID, 'recipeid' : Number(recipe_id)},
		// callback
		function(res) {
			const status = res.status
			console.log(status)
			console.log('Status is: ' + status)
			if (status == 'liked') {
				document.getElementById('like').innerHTML = liked_svg
			} else {
				document.getElementById('like').innerHTML = like_svg
			}
		}
	)
}

// for decode base64 image
function setBase64(file) {
	var reader = new FileReader();
	reader.readAsDataURL(file);
	reader.onload = function () {
	  	console.log(reader.result);
		document.getElementById('base64').value = reader.result
	};
	reader.onerror = function (error) {
	  	console.log('Error: ', error);
	};
}

function rgb2hex(rgb) {
	return rgb.map(function(value) {
		return ("0" + value.toString(16)).slice(-2);
	}).join("");
}

// for extract colors of recipe image
function getColorDots(img_url) {
	console.log(`request GET to /image/color, ${img_url}`)
	res = $.get('/image/color', {'img_url' : img_url},
		// callback
		function(res) {
			const color = res.colors
			console.log(color)
			let a_html = `<a href="/search?color=${rgb2hex(color)}" style="background-color: rgb(${color[0]}, ${color[1]}, ${color[2]})"></a>`

			console.log(a_html)
			document.getElementById("contain-color").innerHTML += a_html
		}
	)
}
