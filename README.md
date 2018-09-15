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
1. python web_scraping_images_redblue.py
or
2. python web_scraping_images_redblue.py -generation 2
or
3. python web_scraping_images_redblue.py -g 3
3.1. Download images and place in a folder: sprites\000Name.png
4. python indexing.py
4.1. Creates an index file of moments of all images: index.pkl
5. python find_screen.py --query screens\gameboy_marowak.jpg
5.1. Creates an image of the object that's found: object.png
6. python whos.py --index index.pkl --object object.png
6.1. Compare the object and print its name: The object is: 'Name'

Referenced:
https://www.pyimagesearch.com/
by Adrian Rosebrock
