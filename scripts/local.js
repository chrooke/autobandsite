function togglePlayPause(song) {
    var image = document.getElementById('ppImage.'+song);
    if (image.src.match("play")) {
        image.src = "./images/Pause.jpg";
	image.alt = "Pause";
	document.getElementById('player.'+song).play()
    } else {
        image.src = "./images/play.jpg";
	image.alt = "Play";
        document.getElementById('player.'+song).pause()
    }
}
