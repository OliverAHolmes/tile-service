import services.make_tile as make_tile
import os

# test_url = 'http://localhost:8080/645465335874aa00066577b2.tif/13/3693/6481/'

x = 6481
y = 3693
z = 13

return_tile = make_tile.return_tile('645465335874aa00066577b2.tif', x, y, z)
os.makedirs(f"maps/645465335874aa00066577b2/{z}/{x}", exist_ok=True)
return_tile.save(f"maps/645465335874aa00066577b2/{z}/{x}/{y}.png", format='PNG')