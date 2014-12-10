# os-phototools

Grown out of a need to do some basic manipulation to photos, I put together a few helpers in python to do some simple tasks. Only tested on Windows.

The module Kygoni is for photo kung-fu. Let's see what's inside:

### Resize

Walks through a directory tree to:

* Strip out extraneous data (but preserving metadata)
* Adjust the resolution and shrink the photo (you don't always need full retina display)

The purpose of this was to take photos that were shot on an iPad and iPhone that might need to be referenced, used, but not necessarily at the capacity as a photographer needs. Reduces size to about 1/10th of the original.

#### Move

A simple tool that walks through a directory tree and moves all those photos to another directory

### Crop and Blur

Examples of blurring and cropping that could be batch done on a group of photos. The PIL library offers plenty of other tools to suite your needs. The current example was developed to crop our, or blur, the watermark stamped on photos with the Theodolite iOS app.
