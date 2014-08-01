NyePy
=====

Python code for Aug 2014 Installation SLURP! (http://slurp-show.tumblr.com/)  by artist Nye Thompson (nyethompson.co.uk)

Runs 20 Aug - 14 Sep '14, London Canal Museum, 12-13 New Wharf Road, London N1 9RT

Runs on a Raspberry with the Raspberry Pi Camera Module.

It will take a snapshot from the camera, then iteratively blend it with the currently displayed picture, and repeat. Various resolutions are configurable, and, instead of updating a single display image, the code can divide the diplay area into varius quadrants (or nonants, or sextuplants...), and cycle through the one it is updating

The result, when the Pi and its camera are set-up inside the art installation (so the camera gets a fixed backgrounds) is that viewers of the installation are able to view themselves as ghosting images on the display area

The scripts reads itself as a file, and displays chunks of its own code, mirrored and aligned to the right, as if read from behind the screen itself.

Makes extensive use of PIL (or indeed Pillow), and Pygame, which I've found a breeze to manage displaying to screen with a minimum of fuss. The capture is done using the Pi's own camera module, but substituting the capture function by one that reads from a USB webcam can allow you to re-create the experience on any machine (provided it has a screen, or can display to a projector, and a webcam)
