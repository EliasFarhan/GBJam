#Kudu Engine

Kudu is a game engine written in python (compatible with 2-3), depending on python-sfml (pygame if not found) and Box2D. It can be embed in Pookoo engine.

It use JSON to store game data like the structure of level and the images of the player animation, or the GUI.

Documentation [here](http://team-kwakwa.com/kudu_doc/index.html)

###Install
Install [python-sfml](http://www.python-sfml.org/)
(or [pygame](http://www.pygame.org/), but deprecated )
and [Box2D](http://code.google.com/p/pybox2d/)

### Create game project
- Create an init JSON file in data/json/init.json who will look like this:
``` {
	"init": "data/json/level.json",
	"screen_size": [1280,720]
} ```

- Create a level JSON file:
``` {
	"images": {
	},
	"physic_object": {
	}
} ```



###TODO
- Editor
- GUI element
- Custom init creation at start