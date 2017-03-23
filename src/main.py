import graph
import imgloader
import imgwriter

il = imgloader.ImageLoader("normal.bmp")
il.show()

x = graph.Graph(il.pixel_map, il.h, il.w)
x.show()

iw = imgwriter.ImageWriter(il.mode, il.pixel_map, (il.w, il.h))
iw.write("out.bmp")
