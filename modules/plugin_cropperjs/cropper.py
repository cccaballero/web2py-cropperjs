
from gluon.sqlhtml import FormWidget
from gluon.validators import IS_EMPTY_OR
from gluon.html import *
from gluon import current
from .cropperutils import camel_to_lisp


class CropperWidget(FormWidget):
    _class = 'upload'

    DEFAULT_WIDTH = '150px'
    ID_DELETE_SUFFIX = '__delete'
    GENERIC_DESCRIPTION = 'file ## download'
    DELETE_FILE = 'delete'

    @classmethod
    def widget(cls, field, value, download_url=None, options=None, **attributes):
        """
        generates a INPUT file tag and Croperjs.

        Optionally provides an A link to the file, including a checkbox so
        the file can be deleted.

        All is wrapped in a DIV.

        see also: `FormWidget.widget`

        Args:
            field: the field
            value: the field value
            download_url: url for the file download (default = None)
            options: cropper.js options
        """

        current.response.files.append(URL('static', 'plugin_cropperjs/cropper.css'))
        current.response.files.append(URL('static', 'plugin_cropperjs/cropper.js'))
        current.response.files.append(URL('static', 'plugin_cropperjs/plugincropper.js'))

        default = dict(_type='file', )
        attr = cls._attributes(field, default, **attributes)

        attr['_class'] = attr['_class'] + ' cropit-image-input'

        name = attr['_name']

        if options:
            options_data = CropperWidget.options_to_data(options)
        else:
            options_data = {}
        options_data['_data-name'] = name

        inp = DIV([
            DIV(IMG(_id="cropper-img-"+name), _class="image-container"),
            INPUT(data={"cropper": "cropper-"+name}, **attr),
            INPUT(_id=name+"_cropper_detail_x", _name=name+"_cropper_detail_x", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_y", _name=name+"_cropper_detail_y", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_width", _name=name+"_cropper_detail_width", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_height", _name=name+"_cropper_detail_height", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_rotate", _name=name+"_cropper_detail_rotate", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_scaleX", _name=name+"_cropper_detail_scaleX", _type="hidden"),
            INPUT(_id=name+"_cropper_detail_scaleY", _name=name+"_cropper_detail_scaleY", _type="hidden"),
            DIV("Select new image", _class="select-image-btn"),
        ], _class="image-cropper-container", **options_data)

        if download_url and value:
            if callable(download_url):
                url = download_url(value)
            else:
                url = download_url + '/' + value
            (br, image) = ('', '')
            if CropperWidget.is_image(value):
                br = BR()
                image = IMG(_src=url, _width=cls.DEFAULT_WIDTH)

            requires = attr["requires"]
            if requires == [] or isinstance(requires, IS_EMPTY_OR):
                inp = DIV(inp,
                          SPAN('[',
                               A(current.T(
                                   CropperWidget.GENERIC_DESCRIPTION), _href=url),
                               '|',
                               INPUT(_type='checkbox',
                                     _name=field.name + cls.ID_DELETE_SUFFIX,
                                     _id=field.name + cls.ID_DELETE_SUFFIX),
                               LABEL(current.T(cls.DELETE_FILE),
                                     _for=field.name + cls.ID_DELETE_SUFFIX,
                                     _style='display:inline'),
                               ']', _style='white-space:nowrap'),
                          br, image)
            else:
                inp = DIV(inp,
                          SPAN('[',
                               A(current.T(cls.GENERIC_DESCRIPTION), _href=url),
                               ']', _style='white-space:nowrap'),
                          br, image)

        return inp

    @classmethod
    def options_to_data(cls, options):
        data = {}
        for key in options:
            data["_data-"+camel_to_lisp(key)] = options[key]
        return data

    @classmethod
    def represent(cls, field, value, download_url=None):
        """
        How to represent the file:

        - with download url and if it is an image: <A href=...><IMG ...></A>
        - otherwise with download url: <A href=...>file</A>
        - otherwise: file

        Args:
            field: the field
            value: the field value
            download_url: url for the file download (default = None)
        """

        inp = current.T(cls.GENERIC_DESCRIPTION)

        if download_url and value:
            if callable(download_url):
                url = download_url(value)
            else:
                url = download_url + '/' + value
            if cls.is_image(value):
                inp = IMG(_src=url, _width=cls.DEFAULT_WIDTH)
            inp = A(inp, _href=url)

        return inp

    @staticmethod
    def is_image(value):
        """
        Tries to check if the filename provided references to an image

        Checking is based on filename extension. Currently recognized:
           gif, png, jp(e)g, bmp

        Args:
            value: filename
        """

        extension = value.split('.')[-1].lower()
        if extension in ['gif', 'png', 'jpg', 'jpeg', 'bmp']:
            return True
        return False
