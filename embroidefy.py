#!/usr/bin/env python

#https://boonepeter.github.io/posts/2020-11-10-spotify-codes/
#https://stackoverflow.com/questions/62121301/encoding-spotify-uri-to-spotify-codes
#https://www.freepatentsonline.com/20180181849.pdf
#https://github.com/spotify/web-api/issues/519

from io import BytesIO
from skimage import io
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import requests
import tkinter as tk
from tkinter import messagebox

class Embroidefy:
    def __init__(self, filename):
        self.metadata = '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <svg xmlns:inkstitch="http://inkstitch.org/namespace" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="640" height="160" viewBox="0 0 400 100" version="1.1" id="svg4121" sodipodi:docname="stitch_absolute.svg" inkscape:label="Spotify Logo" inkscape:version="1.0.2 (e86c8708, 2021-01-15)"> <metadata id="metadata4127"> <rdf:RDF> <cc:Work rdf:about=""> <dc:format>image/svg+xml</dc:format> <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /> <dc:title></dc:title> </cc:Work> </rdf:RDF> <inkstitch:collapse_len_mm /> </metadata> <defs id="defs4125" /> <sodipodi:namedview pagecolor="#ffffff" bordercolor="#666666" borderopacity="1" objecttolerance="10" gridtolerance="10" guidetolerance="10" inkscape:pageopacity="0" inkscape:pageshadow="2" inkscape:window-width="1440" inkscape:window-height="900" id="namedview4123" showgrid="false" inkscape:zoom="0.99044916" inkscape:cx="383.2883" inkscape:cy="66.335772" inkscape:window-x="0" inkscape:window-y="0" inkscape:window-maximized="0" inkscape:current-layer="svg4121" inkscape:document-rotation="0" />'
        self.spotify_logo = '<g id="g4760"><path fill="#000000" d="M 50,20 C 62.133854,20 73.073016,27.309306 77.716178,38.519324 82.359331,49.72932 79.79202,62.632232 71.212126,71.212126 62.632232,79.79202 49.72932,82.359331 38.519324,77.716178 27.309306,73.073016 20,62.133854 20,50 20,33.431458 33.431458,20 50,20" id="path4117" sodipodi:nodetypes="cssssc" style="fill:none;stroke:#000000;stroke-width:2.9375;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" /><path style="fill:none;stroke:#000000;stroke-width:5.4375;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="m 29.361986,41.411481 c 0,0 22.02149,-8.586996 41.965483,4.016498" id="path4715" /><path style="fill:none;stroke:#000000;stroke-width:4.5625;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="m 31.577986,50.967976 c 0,0 18.064553,-7.586445 35.832014,4.032024" id="path4717" /><path style="fill:none;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="m 32.824485,59.970472 c 0,0 16.383051,-6.421438 30.905515,3.229528"  id="path4719" /></g>'
        self.x_pos = [103.355,115.775,128.195,140.625,153.045,165.465,177.885,190.31501,202.735,215.155,227.575,239.995,252.42501,264.84499,277.265,289.68499,302.11501,314.53499,326.95501,339.37499,351.795,364.225,376.64501]
        self.positions = [[44.5,55.5],[41,59],[37.5,62.5],[34,66],[30.5,69.5],[27,73],[23.5,76.5],[20,80]]
        self.uri = self.convert_share_link_to_uri(filename)

    def get_heights(self, filename: str) -> list:
        #print('in get heights')
        #"""Open an image and return a list of the bar heights."""
        # convert to grayscale, then binary
        image = io.imread(filename)
        im = rgb2gray(image)
        binary_im = im > threshold_otsu(im)
        # label connected regions as objects
        labeled = label(binary_im)
        # get the dimensions and positions of bounding box around objects
        bar_dimensions = [r.bbox for r in regionprops(labeled)]
        bar_dimensions.sort(key=lambda x: x[1], reverse=False)
        # the first object (spotify logo) is the max height of the bars
        logo = bar_dimensions[0]
        max_height = logo[2] - logo[0]
        sequence = []
        for bar in bar_dimensions[1:]:
            height = bar[2] - bar[0]
            ratio = height / max_height
            # multiply by 8 to get an octal integer
            ratio *= 8
            ratio //= 1
            # convert to integer (and make 0 based)
            sequence.append(int(ratio - 1))
        #print(sequence)
        return sequence

    def make_path(self, x_pos, position):
        return '<path id="rect4071" style="fill:none;stroke:#000000;stroke-width:5;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M ' + str(x_pos) + ',' + str(position[0]) + ' V ' + str(position[1]) + ' Z" sodipodi:nodetypes="ccc" />'

    def make_whole_path(self, heights):
        #print('in make whole path')
        whole_path = ''
        for index, height in enumerate(heights):
            whole_path += self.make_path(self.x_pos[index], self.positions[height])
        return whole_path

    def save_svg(self, whole_path):
        #print('in save svg')
        f = open('embroidefy_' + self.uri.split(':')[-1] + '.svg', 'w')
        f.write(self.metadata + self.spotify_logo + whole_path + '</svg>')

    def convert_share_link_to_uri(self, share_link):
        print('convert share link to uri')
        if 'http' in share_link:
            media_type = share_link.split('/')[-2]
            uri = share_link.split('/')[-1].split('?')[0]
            return 'spotify:' + media_type + ':' + uri
        else:
            return share_link
    
    def get_code_from_uri(self):
        #print('get code from uri')
        r = requests.get('https://scannables.scdn.co/uri/plain/png/000000/white/640/' + self.uri)
        return r.content
    
    def convert_code(self):
        #print('convert code')
        code = self.get_code_from_uri()
        heights = self.get_heights(BytesIO(code))
        whole_path = self.make_whole_path(heights)
        self.save_svg(whole_path)

def main():
    def handle_focus_in(_):
        entry.delete(0, tk.END)
        entry.config(fg='black')

    def handle_focus_out(_):
        entry.delete(0, tk.END)
        entry.config(fg='grey')
        entry.insert(0, 'spotify:playlist:4HMGMig6Q2MshPzhgPNgdC or https://open.spotify.com/playlist/4HMGMig6Q2MshPzhgPNgdC?si=61b34c9093d04839')

    def convert():
        try:
            Embroidefy(entry.get()).convert_code()
            print('yeet')
            messagebox.showinfo('success', 'svg File for ' + entry.get() + ' created successfully')
        except:
            messagebox.showerror('error', 'Something went wrong.')
    window = tk.Tk()
    window.title('Embroidefy')
    uppertext = tk.Label(text='Welcome to Embroidefy.\nPaste a Spotify URI or Share Link below, then click "CONVERT".\nAn .svg file starting with "embroidefy" will be saved to your computer which you can open in Inkscape.\nYou\'ll still need to save this file as a .pes file before using on your machine, but all the digitization has been taken care of.\nSimply scale or add your own details to the image.', width=100)
    uppertext.pack()
    entry = tk.Entry(width=90, fg='grey')
    entry.insert(0, 'spotify:playlist:4HMGMig6Q2MshPzhgPNgdC or https://open.spotify.com/playlist/4HMGMig6Q2MshPzhgPNgdC?si=61b34c9093d04839')
    entry.bind("<FocusIn>", handle_focus_in)
    entry.bind("<FocusOut>", handle_focus_out)
    entry.pack()
    button = tk.Button(
        text="CONVERT",
        width=20,
        height=2,
        command=convert
    )
    button.pack()
    window.mainloop()

if __name__ == '__main__':
    main()
