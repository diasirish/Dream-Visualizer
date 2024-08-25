import re

text = "Scene 1: University Division\n\nDescription: You find yourself back at the university, but things are different. The university is divided into two wings - a north and a south wing, resembling a boarding school setup. Your classmates from school, including Americans, are present. In your backpack, there is a brick that you carry with you as you navigate from one lesson to another. The atmosphere is bustling with students moving back and forth between classes. You remember names like META and Rochita, and as you attend a biology lesson, you notice the contrast between the emptiness of the room at first and then the sudden influx of students. The scene is set within the distinguished architecture of the university building, with corridors bustling with students shuffling between classes.\n\nScene 2: Poolside Encounter\n\nDescription: After a long day of classes, you and your friend Albert decide to head to the communal pool located within the university's main building. The grand building is split into two wings, each with its own pool - one larger and more leisure-focused, while the other designed for sports activities. As you interact with Albert near the poolside, reminiscing about missed opportunities to surf, the dream transitions seamlessly from the pool to the open sea. The imagery shifts to include crashing waves and the sound of seagulls overhead, creating a serene yet adventurous atmosphere. The focus here lies on the camaraderie between you and Albert as you immerse yourselves in the waters, surrounded by the vastness of the sea.\n\nScene 3: Mountain Ascent\n\nDescription: The dream takes a sudden turn as you and Albert find yourselves scaling rocky mountains together. Armed with a saw-like tool, you demonstrate a sense of urgency and determination as you secure your climb. The landscape becomes rugged and challenging, with each step a precarious yet rewarding venture. As you assist Albert in overcoming obstacles, the tension in the scene heightens as a stone accidently falls, injuring Albert's hand. The focus shifts to the personal connection and vulnerability shared between you and Albert amidst the harsh terrain, emphasizing resilience and mutual support in the face of adversity.\n\nScene 4: Awakening Clarity\n\nDescription: The dream culminates in a moment of realization and awakening as the alarm clock disrupts the vivid imagery of the mountain ascent. The final scene captures a mix of relief and introspection as you are jolted from the dream state, carrying with you the emotions and lessons learned throughout the dream. The transition from the intense mountain climb to the abrupt wakefulness serves as a poignant reminder of the boundaries between dream and reality, leaving a lingering sense of resolve and revelation. The imagery here juxtaposes the surreal mountain landscape with the familiarity of the alarm clock, symbolizing the duality of dreams and waking life."

scenes = {}
scene_blocks = re.findall(r'(Scene \d+:\s*.*?Description:.*?)(?=Scene \d+:|$)', text, re.DOTALL)

for block in scene_blocks:
    # Extract the scene number using regex
    scene_number = int(re.search(r'Scene (\d+)', block).group(1))
    
    # Extract the description part after "Description:"
    description = re.search(r'Description:\s*(.*)', block, re.DOTALL).group(1).strip()
    
    # Add the scene number and its description to the dictionary
    scenes[scene_number] = description

print(scenes)
print(scenes.keys())
