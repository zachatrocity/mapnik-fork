import mapnik

merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

mapfile = "osm.xml"

m = mapnik.Map(600,300)
mapnik.load_map(m,mapfile)
m.srs = longlat.params()
bounds = (-92.493874, 34.626320, -92.15654, 34.818401)

#create your style
s = mapnik.Style()
r = mapnik.Rule()
point_sym = mapnik.PointSymbolizer()
point_sym.filename = './symbols/airport.p.16.png'
r.symbols.append(point_sym) # add the symbolizer to the rule object
s.rules.append(r) # now add the rule to the style and we're done
m.append_style('airport point', s)

#add your data source.. usually would be a PostgreSQL/SQLite database
ds = mapnik.MemoryDatasource()
f = mapnik.Feature(mapnik.Context(), 1)
f.add_geometries_from_wkt("POINT(-92.289595 34.746481)")
ds.add_feature(f)

#create the layer and add the data
player = mapnik.Layer('airport_layer')
player.srs = longlat.params()
player.datasource = ds
player.styles.append('airport point')
m.layers.append(player)
m.zoom_all()

if hasattr(mapnik,'Box2d'):
    bbox = mapnik.Box2d(*bounds)
else:
    bbox = mapnik.Envelope(*bounds)

# Our bounds above are in long/lat, but our map
# is in spherical mercator, so we need to transform
# the bounding box to mercator to properly position
# the Map when we call `zoom_to_box()`
transform = mapnik.ProjTransform(longlat,merc)
merc_bbox = transform.forward(bbox)

# Mapnik internally will fix the aspect ratio of the bounding box
# to match the aspect ratio of the target image width and height
# This behavior is controlled by setting the `m.aspect_fix_mode`
# and defaults to GROW_BBOX, but you can also change it to alter
# the target image size by setting aspect_fix_mode to GROW_CANVAS
#m.aspect_fix_mode = mapnik.GROW_CANVAS
# Note: aspect_fix_mode is only available in Mapnik >= 0.6.0
m.zoom_to_box(merc_bbox)

mapnik.render_to_file(m,'world.png', 'png')
print "rendered image to 'world.png'"