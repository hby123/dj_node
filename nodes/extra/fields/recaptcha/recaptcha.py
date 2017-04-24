import os
import random
import sys

from django import forms

import dj_node
from dj_node.nodes.extra.fields.recaptcha.var import recaptcha_dict

sys.path.append('c:\WINDOWS\Fonts\RAVIE')
sys.path.append('/etc/fonts/fonts.conf')

class XRecaptchaWidget(forms.Widget):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    def __init__(self, *args, **kwargs):
        self.user = None
        super(XRecaptchaWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):           
        path, i = XVeifyHuman.get_random_image();
        html = "<img src=\"%s\" class=\"recap\" ></img>" % path
        html = html + "<input type=\"text\" id=\"id_verify_human\" name=\"verify_human\" class=\"%s\" placeholder=\"%s\"></input>" \
                % (self.recaptcha_class, self.recaptcha_instruction)
        html = html + "<input type=\"hidden\" id=\"id_verify_human_path\" name=\"verify_human_path\" value=\"%s\" ></input>" % i;
        return html
        
    def value_from_datadict(self, data, files, name):
            return [data.get('verify_human', None), 
                    data.get('verify_human_path', None)]

class XRecaptchaField(forms.Field):
    widget = XRecaptchaWidget

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
       super(XRecaptchaField, self).__init__(*args, **kwargs)
  
    def clean(self, value):
        if len(value) == 2:
                user_value = value[0]
                internal_id = value[1]    
                if     internal_id != '' and internal_id != None:       
                        internal_value = XVeifyHuman.get_image_value(internal_id)                        
                        if user_value != None and user_value != "":
                            if user_value == internal_value: 
                                return True
        raise forms.ValidationError("Please enter the letters as shown.")
              
class XVeifyHuman(object):
    @staticmethod
    def get_image_value(image_id):
        value = recaptcha_dict[int(image_id)]
        return value
  
    @staticmethod
    def get_random_image():
           i = random.randint(1, len(recaptcha_dict.keys()))
           return "/static/dj_node/recaptcha/%d.jpg" % ( i ), i
           
    @staticmethod
    def gen_captcha(text, file_name, fmt='JPEG', fnt="RAVIE.TTF", fnt_sz=22):
          from PIL import Image, ImageFont, ImageDraw

          new_text = "";
          for i in range(0, len(text)):
              new_text = new_text + text[i] + " "
          text = new_text 

          # use a truetype font
          img = Image.new('RGB', (380, 65), (255, 255, 255))
          draw = ImageDraw.Draw(img)
          font = ImageFont.truetype(fnt, 30)
          draw.text((35, 35), text, font=font, fill=(0, 0, 0,255))

          img.save(file_name, format=fmt)

    @staticmethod
    def write_captcha_list():
        for key in recaptcha_dict.keys():
            word = recaptcha_dict[key]
            dj_node_path = os.path.dirname(dj_node.__file__)
            path = os.path.join(dj_node_path, 'static', 'recaptcha', str(key) + ".jpg")
            XVeifyHuman.gen_captcha(word, path)