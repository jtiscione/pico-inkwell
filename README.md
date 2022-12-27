# E-Paper Frame

#### Remotely control an e-ink display with a Raspberry Pi Pico W.

This project will run a little HTTP server on your local network.
It serves up a crude MS Paint clone written in JavaScript, written specifically
for an e-ink display.

You can paste an image, scale and place it, and perform Floyd Steinberg
dithering on the result. There are also tools for scribbling, drawing boxes,
and adding text.

When you are ready you can render the image on the display, the app will send the
encoded image data to the Pico W using a series of HTTP POST requests.

To identify the e-ink device, the Pico W filesystem must contain a file named device.txt
containing one of the following device codes:

EPD_2in9_B       (for the 2.9 inch red/black/white display)
EPD_3in7         (for the 3.7 inch black / dark gray / light gray / white display)
EPD_5in65        (for the 5.65 inch 7 color aCEP dsplay)

In addition it looks for a wpa_supplicant.conf file to get the wireless configuration.
This file must be on the Pico W and only needs to contain two lines of the form:

ssid="My_SSID"
psk="Password123"

The remaining files that must be present on the Pico W are index.html, index.css, index.js,
main.py, and lib/epd.py.