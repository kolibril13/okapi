// @ts-check

var version_number =  "v0.0.1"
var whole_string = "version ".concat(version_number)

document.getElementById('version_number').innerHTML = whole_string;


var request1 = new XMLHttpRequest();
request1.open("GET", "imgs/array_gallery.json", false);
request1.send(null);
var jsonData1 = JSON.parse(request1.responseText);
document.writeln(' <h1>2D Arrays</h1>')
for (let key of Object.keys(jsonData1)) {
    document.write(`<img src='imgs/${key}' alt= '${jsonData1[key]}' onclick='myFunction(this);' class='image'> `);
}


var request4 = new XMLHttpRequest();
request4.open("GET", "imgs/structuing_elements.json", false);
request4.send(null);
var jsonData4 = JSON.parse(request4.responseText);
document.writeln(' <h1>3D Structuing Elements</h1>')
for (let key of Object.keys(jsonData4)) {
    document.write(`<img src='imgs/${key}' alt= '${jsonData4[key]}' onclick='myFunction(this);' class='imagebig'> `);
}

// add copy button to images
function myFunction(imgs) {
    var name = imgs.alt;
    navigator.clipboard.writeText(name);
    document.getElementById("info_field").innerHTML = name + " \n<b>is now copied to clipboard.</b>"
}
