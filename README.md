# web2py-cropperjs
[Cropper.js](https://fengyuanchen.github.io/cropperjs/) integration in the web2py framework

## Installation

- Download the last plugin installer (.w2p file) and install it via the web2py interface.

## Usage

```python
from plugin_cropperjs import cropper # Import the cropper module

db.define_table('my_table',
                Field('image','upload',
                      widget=cropper.CropperWidget.widget # Include the Cropper.js widget in the form field
                      )

```

On new forms generated there will be available the cropper.js widget including the next hidden fields:

- image_cropper_detail_x
- image_cropper_detail_y
- image_cropper_detail_width
- image_cropper_detail_height
- image_cropper_detail_rotate
- image_cropper_detail_scaleX
- image_cropper_detail_scaleY

## Cropping images server side using PIL/Pillow

web2py-cropperjs includes utilities for cropping the uploaded images server-side using PIL/Pillow, in the required controller you can use:

```python
from cgi import FieldStorage
from plugin_cropperjs import cropperutils

def grid():
    # Find if is a grid 'new' or 'edit' form
    if request.args(0) in ['new', 'edit']:
        # Check if there is a file uploaded
        if isinstance(request.vars.image, FieldStorage):
            # Obtain the required cropper field values
            x = request.vars.image_cropper_detail_x
            y = request.vars.image_cropper_detail_y
            w = request.vars.image_cropper_detail_width
            h = request.vars.image_cropper_detail_height
            rotate = request.vars.image_cropper_detail_rotate
            # Replace the original image with the cropped one
            request.vars.image = cropperutils.crop_image(request.vars.image, x, y, w, h, rotate)
    grid = SQLFORM.grid(db.my_table)
    return dict(grid=grid)

```

## Passing options to Cropper.js

Options can be passed to Cropper.js in the next way:

```python
from plugin_cropperjs import cropper

db.define_table('my_table',
                Field('image','upload',
                      # Include widget as lamda function for passing arguments
                      widget=lambda field,value,download_url: cropper.CropperWidget.widget(
                          field,
                          value,
                          download_url,
                          # Include Cropper.js options
                          options={
                              'aspectRatio': 16/9,
                              'movable': 'false',
                              'zoomable': 'false',
                              'rotatable': 'false',
                              'scalable': 'false'
                          }
                      ))

```
