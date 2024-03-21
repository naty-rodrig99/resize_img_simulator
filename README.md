# Resize Image Simulator

These are the formulas and steps followed to simulate how to resize images by using the bilinear interpolation technique.
1. Calculate the proportional distance between the target pixel’s position and position of the nearest pixel in the original grid:
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/b9cd04c4-f44b-4651-a7c2-112b31bba737" width="300">
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/f0cc1c5d-f1bf-4ca1-b597-3f592e72d411" width="300">

2. Calculate the x and y indexes of the nearest pixel in the original image to the target pixel in the output image:
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/0a97eb09-a681-4cd7-a6de-843f240ac074" width="150">
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/2cf45628-1c1e-42d5-8d7c-84f5c1bc398c" width="150">

3. Calculate the fractional parts of the target pixel’s position relative to the position of the nearest pixel in the original grid:
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/a8a0c27f-73f3-490a-929c-e888e0aaca2e" width="150">
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/90df56fc-5b75-4234-8e3f-fc659fb9c77c" width="150">

3. For each color channel: 2 interpolations in x-direction, one in y-direction
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/5e9ae33e-59db-43eb-b2a3-1db8a6d7f8aa" width="320">
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/dffb7bd4-c310-452d-803d-e1db238d8d64" width="320">
<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/d0e74464-29dc-4a54-a2ac-46d8bfcae193" width="320">

The resulting interpolated intensity values for each color channel are combined to form the final RGB color value for the target pixel position.

<img src= "https://gits-15.sys.kth.se/storage/user/23835/files/757e1ff6-ff15-44de-98d2-09f260597506" width="300">

