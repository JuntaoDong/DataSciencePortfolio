# Computer Vision for Sports Advertising Leveraging Models Built with PowerAI Vision

## Acknowlegements

Special thanks to Mr. Chris Eaton for providing the original material and Mr. Neal Rudnick for the presentation and kindly help. Also thanks to IBM Cincinnati for holding such a great workshop.

## Introduction

This hands-on lab provides the understanding and hands-on experience to be able to demonstrate PowerAI Vision to a client. The lab provides more than just the ability to label data and train a model for object detection or image classification. But more importantly, this lab gives you some hands-on experience with a Python application that performs inferencing with the model you create with PowerAI Vision and lets you do some interesting things with those detected objects.

We use a Japan vs. Australia football game highlight video for our example but you can do this with any video. We build a model that can detect advertisers' logo around the field. That part is simple enough and is an interesting demonstration. But then we take it one step further. By using a fairly simple Python application (run via a Jupyter Notebook), you will be able to take a second highlight video (that has the same logos) and break that video down into frames and call your PowerAI Vision built model to find the logos of interest and label them. The best part, however, is that the application will also keep track of how long each logo was visible during the video. Imagine the use case for tracking how much television screen time a given sponsor is getting during a game and charging them based not for the space but for the time they actually appeared on screen.

This lab helps you take a video that looks like this:

![input](./input.gif)

And turn it into this:

![output](./output.gif)

## Lab Environment

In this lab we are using PowerAI Vision 1.1.3 to build and train a model for sports advertising object detection. We will also use Python (version 3.7) in a Jupyter Notebook to execute the sample application to build a video with the detected objects labeled inside the video. Note that we are only using the Python application to break down the video into frames, pass those frames into PowerAI for inferencing using a REST API, and then getting back a JSON document with the objects detected within the frames. There is no need for AI frameworks on your laptop in this hands-on because all of the deep learning (DL) work is being done on the PowerAI server side.

You need to pull down the Docker Container from the Docker Hub. Please type the following command in prompt:

```
docker pull nrudnick/soccer_lab:base2
```