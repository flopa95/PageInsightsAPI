function addHighlight(element) {
    if (parseInt(element.innerHTML) > 80) {
        element.classList.add("highlight");
    } else if (parseInt(element.innerHTML) > 60) {
        element.classList.add("orange-highlight");
    } else {
        element.classList.add("red-highlight");
    }
}

function detectIE() {
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE ');

    if (msie > 0) {
        // IE 10 or older => return version number
        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
    }

    var trident = ua.indexOf('Trident/');
    if (trident > 0) {
        // IE 11 => return version number
        var rv = ua.indexOf('rv:');
        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
    }

    var edge = ua.indexOf('Edge/');
    if (edge > 0) {
        // Edge (IE 12+) => return version number
        return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
    }

    // other browser
    return false;
}

var desktop_score = document.getElementById("desktop_score");
var mobile_score = document.getElementById("mobile_score");
var version = detectIE();

addHighlight(desktop_score);
addHighlight(mobile_score);

if (version != false) {
    var tags = document.getElementsByTagName("summary");
    var idx;
    for (idx = 0; idx < tags.length; idx++) {
        tags[idx].classList.add("hidden");
    };
}
