# 1bit gui

`1bit` lets you easily encode your favourite images into [OLED
128x64](https://create.arduino.cc/projecthub/najad/interfacing-and-displaying-images-on-oled-59344a) friendly byte array.

![1bit GIF Demo](demo/demo.gif)

### Why?

Most tools I found required Internet connection. I needed something small, compact and usable offline. Current version allows you to preview the
end result.

### Installation

Git clone this repo and build with poetry.

### Usage

Execute `main.py`.

### Future plans

Add input for threshold values to be able to specify point of conversion between white and black pixels. Without it some
images are not converted properly causing low visiblity.
