# demo.python.zernike.moments
Testing Zernike moments a powerfull shape descriptor, based on Zernike polynomials

In mathematics, the Zernike polynomials are a sequence of polynomials that are orthogonal on the unit disk.

Image processing and computer vision techniques such as:
* Edge detection
* Thresholding
* Perspective warping

We can abstractly represent the image using only a list of numbers (image feature vector).

Python Libraries You Will Need:
* Requests
* BeautifulSoup (bs4 web scraping)
* NumPy
* SciPy
* Scikit-Image
* OpenCV (with bindings)

The steps:
1. Download sprites (a dataset of images)
2. Quantify sprites in terms of their outline (shape)
2. Process the numeric data
3. Train and evaluate learners
4. Plot and compare results

Image moments:
* Calculate the centroid (the center of the object, in terms of x, y coordinates);
* Calculate moments based on the contour of an image.
The scaling and translation of the object in the image:
* Depending on where the object is translated in the image, moments will be different;
* Depending on how large or small (the object is scaled) in the image, moments will be different.
To avoid descriptors with different values based on the translation and scaling:
* Perform segmentation the foreground from the background;
* Form a tight bounding box around the object and crop it out;
* Translation invariance!
* Resize the object to a constant NxM pixels;
* Scale invariance!

The steps of Execution:
>> python web_scraping_images_redblue.py
# Download images and place in a folder: spritesRedBlue\000Name.png
>> python indexing.py
# Creates an index file of moments of all images: index.pkl
>> python find_screen.py -- screen01.png
# Creates an image of the object that's found: object.png
>> python whos.py -- object.png
# Compare the object and print its name: The object is: 'Name'

Referenced:
https://www.pyimagesearch.com/
by Adrian Rosebrock