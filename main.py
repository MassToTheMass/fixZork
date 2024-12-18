import pygame as py
py.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = py.display.set_mode(size, py.RESIZABLE)

clock = py.time.Clock()

current_location = "Observation Deck"

#FONT
line_spacing = 40
typing_buffer = ""
typed_text = "> "
message = ""
display_lines = []

description_given = False

font_path = "Stardew_Valley.ttf" 
font_size = 30
font = py.font.Font(font_path, font_size)
max_line_width = SCREEN_WIDTH - 80

def wrap_text(text, font, max_width):
  lines = text.split("\n")
  wrapped_lines = []
  for line in lines:
      words = line.split(" ")
      current_line = ""
      for word in words:
          test_line = current_line + word + " "
          if font.size(test_line)[0] <= max_width:
              current_line = test_line
          else:
              wrapped_lines.append(current_line.strip())
              current_line = word + " "
      if current_line:
          wrapped_lines.append(current_line.strip())
  return wrapped_lines

#KEY WORDS
def key_words(user_input):
  words = user_input.lower().strip().split()
  keywords = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest", "climb", "up", "down", "unlock", "yes", "no", "pry", "bar", "use"]
  keywords = [word for word in words if word in keywords]
  print(keywords)
  return keywords

def action (keywords):
  global current_location, description_given, message
  if keywords == []:
      message = "I didn't understand that. Enter a valid action."
      return
  verb = keywords[0]
  destination = location[verb]
  current_location = destination
  description_given = False

#INVENTORY
inventory = ["captains_key", "pry_bar"]

#DICTIONARY
map = {
"Opening Description": {
  "description": "As you slowly come to consciousness, your heart thrums in your ears and the blurry shadows resolve. You are tangled in rope and splintered wood, and somewhere above you black birds circle. There is a pry bar near you. \nYou lie in the center of a once sky-bound ship, now a hulking, twisted monument to a failed journey. You are alone, surrounded by a jagged wasteland of rocks and dust. The quiet stillness is broken only by the distant howl of the wind, and metal creaking somewhere to your east...\n",
  "pry bar": "You twist your body and extend your arm out just far enough to grab the pry bar. Maybe you can use this to get out from under the wreckage.\n", #inventory.append("pry_bar")
  "use pry bar": "You manage to wedge the pry bar between you and the wood that is pinning your legs, and you barely wriggle out from under the wreckage before it comes crashing down again, burying the pry bar back under it. You are now standing." #inventory.remove("pry_bar") and current_location = "Observation Deck"
  # ^ if pry_bar in inventory
},
#DECK 1
"Observation Deck": {
   "description": "You are standing on the observation deck. The foremast is splintered, and half of it has come crashing down, splintering a rift through the ship. The floorboards groan with each step, and black, hawk-like birds sort through the wreckage, picking at the gore.\nThe door to the captain's quarters lies to your west. You stand at the base of the crow's nest. To your south is a set of stairs leading further into the airship. To the east are more stairs leading to the bow of the ship.\n", 
   #actions
   "west": "Captain's Door",
   "south": "Crew's Quarters",
   "down": "Crew's Quarters",
   "east": "Ship Bow",
   "climb": "Crow's Nest", 
   "up": "Crow's Nest", 
},
"Crow's Nest": {
   "description": "CROW",
   #actions
   "down": "Observation Deck",
},
"Captain's Door": {
   "description": (
       "Would you like to unlock the door?" if "captains_key" in inventory
       else "The door is locked. You will need a key to enter here.\nReturn to Observation Deck: east\n"
       ),
       "east": "Observation Deck",
       "no": "Observation Deck",
       "yes": "Captain's Quarters",
       "unlock": "Captain's Quarters",
},
"Captain's Quarters": {
   "description": "The room is in disarray: Dark ink grimly splatters across and drips down from the writing desk, and sand from a broken hourglass is scattered across the floor alongside papers and maps. Books and scrolls are strewn about, pages fluttering in the breeze that flows through a broken porthole.\nA crooked portrait of a sunny old man with dusty hair, salty eyes, and a tilted grin overlooks the chaos. This man seems familiar to you, but you can't remember his name. You stare at the painting a long while trying to recall, then give up.\nOn the desk, the captain's logbook lies open, its pages smudged with ink, offering cryptic clues to the ship's final moments.\n",
   #actions
   "east": "Observation Deck",
   "read map": "the map says this",
},
"Ship Bow": {
   "description": "The base of the foremast is splintered",
   #actions
   "west": "Observation Deck",
},
#DECK 2
"Crew's Quarters": {
      "description": "AHHHHHH",
      #actions
      "north": "Observation Deck",
      "up": "Observation Deck",
  },
}
#MAIN LOOP 
running = True
while running:
   screen.fill(BLACK)
   for event in py.event.get():
      if event.type == py.QUIT:
          running = False

      elif event.type == py.VIDEORESIZE:
          screen = py.display.set_mode(event.size, py.RESIZABLE)
          max_line_width = event.w - 80 

      elif event.type == py.KEYDOWN:
          if event.key == py.K_RETURN:
              user_input = key_words(typed_text)
              action(user_input)
              typed_text = ">"
          elif event.key == py.K_BACKSPACE:
                  if len(typed_text) > 1:
                      typed_text = typed_text[:-1]
          else:
              typed_text += event.unicode
   location = map[current_location]
   if not description_given:
       message = location["description"]
       description_given = True
   y_offset = 40
   for line in wrap_text(message, font, max_line_width):
      computer_surface = font.render(line, True, WHITE)
      screen.blit(computer_surface, (40, y_offset))
      y_offset += line_spacing
   for line in wrap_text(typed_text, font, max_line_width):
      typed_surface = font.render(line, True, WHITE)
      screen.blit(typed_surface, (40, y_offset))
      y_offset += line_spacing
   location_title = font.render(str(current_location), True, BLACK, WHITE)
   screen.blit(location_title, (40, 0))
   py.display.flip()
   clock.tick(60)