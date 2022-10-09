# Hand Tracker

This is a python script using OpenCV and Google's MediaPipe to track hand signs.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install OpenCV and MediaPipe.

```bash
pip install -r requirements.txt
```

## Usage
Using mediapipe to label landmarks with an id can be used to compare others, thus allowing you to find patterns within a hand. 

![alt text](examples/ids.png)

There is also a function called "distance" that compares 2 landmark ids and finds a distance value between them.
```python
distance(5,8) #compares distance from landmark 5 to landmark 8
```
Using the distance between 2 landmarks you can see for example, if 2 fingers are touching. This can be expanded upon by using it to check for hand signs.
```python
#see if pointer finger and thumb are touching, thus making an OK sign
if distance(8, 4) < 40 + scalar and distance(8, 12) > 50 + scalar and distance(12, 16) < 60 + scalar: 
```

```python
#check if all fingers are touching palm, thus making a fist
if distance(8,5)<30+scalar and distance(12,9)<30+scalar and distance(16,13)<30+scalar and distance(20,17)<30+scalar:
```
You can use these checks to write over the image with OpenCV's ```cv2.putText``` function. This can be used to display text when a hand sign is detected.
## Extra
You may notice a variable named "scalar" being used. This is used in addition with the other file, named baseline- which creates a baseline image of your hand to more accurately scale at distance.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[The Unlicense](https://choosealicense.com/licenses/unlicense/)
