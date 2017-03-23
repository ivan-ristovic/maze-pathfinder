import graph
import imgloader

il = imgloader.ImageLoader("a.bmp")
il.show()
x = graph.Graph(il.pixel_map, il.h, il.w)
x.show()
