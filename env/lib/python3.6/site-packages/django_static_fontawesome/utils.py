import os
import glob

app_root = os.path.dirname(__file__)
brand_icons_folder = os.path.abspath(os.path.join(app_root, "./static/fontawesome/svgs/brands/"))
regular_icons_folder = os.path.abspath(os.path.join(app_root, "./static/fontawesome/svgs/regular/"))
solid_icons_folder = os.path.abspath(os.path.join(app_root, "./static/fontawesome/svgs/solid/"))


def get_solid_icons():
    return sorted(["fa-" + os.path.splitext(os.path.basename(x))[0] for x in glob.glob(solid_icons_folder+"/*.svg")])

def get_brand_icons():
    return sorted(["fa-" + os.path.splitext(os.path.basename(x))[0] for x in glob.glob(brand_icons_folder+"/*.svg")])

def get_regular_icons():
    return sorted(["fa-" + os.path.splitext(os.path.basename(x))[0] for x in glob.glob(regular_icons_folder+"/*.svg")])

