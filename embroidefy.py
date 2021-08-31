# https://scannables.scdn.co/uri/plain/[format]/[background-color-in-hex]/[code-color-in-text]/[size]/[spotify-URI]

#URI: 1LzNfuep1bnAUR9skqdHCK

#import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials


#Here's how this is going to go down

# 1)
# I need a GUI with:
# Input for spotify data and colors (hex selector?)
#

# CodeGrabber
# takes:
# URI (or some form), maybe eventually I can have it search, for now I'll include instructions for getting there
# - color of background
# - color of code
# returns: svg file

#embroidery converter
# puts svg into inkscape, converts

#conversion process is:
# poop into inkscape
# convert to path
# break into pieces
# later: make lines satin stitch?
# export as pes
# listo

import sys
import requests
import shutil

def getCode(uri, background_color = '000000', color = 'white', size = '640', type = 'svg'):
    image_url = "https://scannables.scdn.co/uri/plain/" + type + "/" + background_color + '/' + color + '/' + size + '/' + 'spotify:track:' + uri
    print(image_url)
#    filename = image_url.split("/")[-1] + '.' + type #TODO: this could be an API request for the name for better file naming
    filename = "spotify.svg"
    r = requests.get(image_url, stream = True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f: #TODO: how to get this into a folder?
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')


getCode(sys.argv[1])

#image_url = "https://cdn.pixabay.com/photo/2020/02/06/09/39/summer-4823612_960_720.jpg"
#filename = image_url.split("/")[-1]
#
## Open the url image, set stream to True, this will return the stream content.
#r = requests.get(image_url, stream = True)
#
## Check if the image was retrieved successfully
#if r.status_code == 200:
#    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
#    r.raw.decode_content = True
#
#    # Open a local file with wb ( write binary ) permission.
#    with open(filename,'wb') as f:
#        shutil.copyfileobj(r.raw, f)
#
#    print('Image sucessfully Downloaded: ',filename)
#else:
#    print('Image Couldn\'t be retreived')


#org.inkstitch.lettering_generate_json.en_US: Generate JSON...
#org.inkstitch.lettering_generate_json.en_US.noprefs: Generate JSON (No preferences)
#org.inkstitch.embroider.en_US: Embroider...
#org.inkstitch.embroider.en_US.noprefs: Embroider (No preferences)
#org.inkstitch.convert_to_satin.en_US: Convert Line to Satin
#org.inkstitch.convert_to_satin.en_US.noprefs: Convert Line to Satin (No preferences)
#org.inkstitch.troubleshoot.en_US: Troubleshoot Objects
#org.inkstitch.troubleshoot.en_US.noprefs: Troubleshoot Objects (No preferences)
#org.inkstitch.cleanup.en_US: Cleanup Document...
#org.inkstitch.cleanup.en_US.noprefs: Cleanup Document (No preferences)
#org.inkstitch.flip_satins.en_US: Flip Satin Column Rails
#org.inkstitch.flip_satins.en_US.noprefs: Flip Satin Column Rails (No preferences)
#org.inkstitch.remove_embroidery_settings.en_US: Remove embroidery settings...
#org.inkstitch.remove_embroidery_settings.en_US.noprefs: Remove embroidery settings (No preferences)
#org.inkstitch.params.en_US: Params
#org.inkstitch.params.en_US.noprefs: Params (No preferences)
#org.inkstitch.install.en_US: Install thread color palettes for Inkscape
#org.inkstitch.install.en_US.noprefs: Install thread color palettes for Inkscape (No preferences)
#org.inkstitch.cut_satin.en_US: Cut Satin Column
#org.inkstitch.cut_satin.en_US.noprefs: Cut Satin Column (No preferences)
#org.inkstitch.commands.en_US: Attach Commands to Selected Objects...
#org.inkstitch.commands.en_US.noprefs: Attach Commands to Selected Objects (No preferences)
#org.inkstitch.import_threadlist.en_US: Import Threadlist...
#org.inkstitch.import_threadlist.en_US.noprefs: Import Threadlist (No preferences)
#org.inkstitch.auto_satin.en_US: Auto-Route Satin Columns...
#org.inkstitch.auto_satin.en_US.noprefs: Auto-Route Satin Columns (No preferences)
#org.inkstitch.layer_commands.en_US: Add Layer Commands...
#org.inkstitch.layer_commands.en_US.noprefs: Add Layer Commands (No preferences)
#org.inkstitch.stitch_plan_preview.en_US: Stitch Plan Preview
#org.inkstitch.stitch_plan_preview.en_US.noprefs: Stitch Plan Preview (No preferences)
#org.inkstitch.embroider_settings.en_US: Preferences...
#org.inkstitch.embroider_settings.en_US.noprefs: Preferences (No preferences)
#org.inkstitch.simulator.en_US: Simulator / Realistic Preview
#org.inkstitch.simulator.en_US.noprefs: Simulator / Realistic Preview (No preferences)
#org.inkstitch.print.en_US: PDF Export
#org.inkstitch.print.en_US.noprefs: PDF Export (No preferences)
#org.inkstitch.break_apart.en_US: Break Apart Fill Objects...
#org.inkstitch.break_apart.en_US.noprefs: Break Apart Fill Objects (No preferences)
#org.inkstitch.lettering.en_US: Lettering
#org.inkstitch.lettering.en_US.noprefs: Lettering (No preferences)
#org.inkstitch.duplicate_params.en_US: Duplicate Params
#org.inkstitch.duplicate_params.en_US.noprefs: Duplicate Params (No preferences)
#org.inkstitch.lettering_custom_font_dir.en_US: Custom font directory...
#org.inkstitch.lettering_custom_font_dir.en_US.noprefs: Custom font directory (No preferences)
#org.inkstitch.global_commands.en_US: Add Commands...
#org.inkstitch.global_commands.en_US.noprefs: Add Commands (No preferences)
#org.inkstitch.reorder.en_US: Re-stack objects in order of selection
#org.inkstitch.reorder.en_US.noprefs: Re-stack objects in order of selection (No preferences)
#org.inkstitch.lettering_remove_kerning.en_US: Remove Kerning...
#org.inkstitch.lettering_remove_kerning.en_US.noprefs: Remove Kerning (No preferences)
#org.inkstitch.about.en_US: About...
#org.inkstitch.about.en_US.noprefs: About (No preferences)

# /Applications/Inkscape.app/Contents/MacOS/inkscape --export-type="pes" 1LzNfuep1bnAUR9skqdHCK.svg


# /Applications/Inkscape.app/Contents/MacOS/inkscape --actions="select-all; object-to-path; verb: FileSaveACopy: test.pes; FileClose" 1LzNfuep1bnAUR9skqdHCK.svg

#import svg
#select all
#object-to-path
#save as .pes
