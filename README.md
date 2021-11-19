# 1bit gui

`1bit gui` lets you easily transform your favourite images into [OLED
128x64](https://create.arduino.cc/projecthub/najad/interfacing-and-displaying-images-on-oled-59344a) friendly byte array straight from your
local environement. 

![1bit GIF Demo](demo/demo.gif)

Contents
========

 * [Why?](#why)
 * [Installation](#installation)
 * [Usage](#usage)
 * [Future plans](#future-plans)

### Why?

Most tools I found required Internet connection and provided too many features. I needed something small that could work
alongside my Arduino IDE, and more importantly, something that'd work offline. Current version allows you to preview the
end result.

### Installation

Git clone this repo and build with poetry.

### Usage

Execute `main.py`.

### Future plans

Add input for threshold values to be able to specify point of conversion between white and black pixels. Without it some
images are not converted properly causing low visiblity.
