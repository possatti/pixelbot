pixelbot
========

This is an attempt to create bots for the pixelcanvas.io site. It is very experimental and not ready at all. Currently the bot can't skip the cooldown, and can't solve the captchas for you. But it is still useful because the bot can place each pixel right after the other automatically. Requiring very little attention from you, hopefully.

## How to use it

Prepare an image that you want to paint on pixelcanvas.io. I suggest using low resolution images. The bigger the image, the longer it will take do paint it. Transparent pixels on the image will be ignored. And pixels with colors that don't match the available color palette will be drawn using the most similar color available.

Alternatively you can use a text file, where numbers represent colors and space characters are empty spaces (nothing will be drawn on that position). Notice that only a limited set of colors are available (from 0 to 9). You can take `examples/pixelbot.txt` as an example of that.

Now you will use the `botfactory.py` script to produce your bot. For that you will need the image/text file; the coordinates on pixelcanvas.io where you want to draw; and your fingerprint. You can find your fingerprint by painting a single pixel and watching the POST request. Your fingerprint will be there. And make sure you have the necessary dependencies installed for the script to work.

After using the `botfactory.py`, a bot will be created in a JavaScript file right next to the original image/text file. You should now copy the content of the produced script, open pixelcanvas.io, open the browser's console, and paste the script on the console.

So, for example, we have drawn a very beautiful image that we want to paint on pixelcanvas,io. Say `examples/space_invaders.png` for example. We open pixelcanvas.io on Firefox, press F12, go to the Network tab, reload the page, paint a pixel, inspect the POST request to find our fingerprint. Then we decide where we want to paint the image: 500 400. We then create the bot with `python botfactory.py examples/space_invaders.png 500 400 30c435861c11298f63df83d2191da1ba`. Now we copy the content of `examples/space_invaders.js` (**js**). With firefox still open, we go to the Console tab, paste our script there, and click enter. Now you sit down and relax.

From time to time you should be asked to solve a captcha. In my experience this is very rare. And the bot will throw a notification to let you know you should interfere. It will also log what it is doing on the console window.

I want your attention on more time for the fact that this doesn't work all the time. Sometimes it does, sometimes it does not. Try your luck. :)

## Dependencies

The `botfactory.py` script needs Pillow installed (pip install pillow). I made the script for Python 3, but it should also work with Python 2.

## Contributing

Every contribution is welcome. But before submitting large chunks of code, it is better to discuss things on a Issue before. Even if you don't want to contribute with code, ideas on how to make this bot work are welcome. You can open a Issue for that too.
