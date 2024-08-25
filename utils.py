import re

def extract_scenes(text):
    """ """
    scenes = {}
    scene_blocks = re.findall(r'(Scene \d+:\s*.*?Description:.*?)(?=Scene \d+:|$)', text, re.DOTALL)

    for block in scene_blocks:
        if block.startswith("Scene"):
            scene_number = int(re.search(r'Scene (\d+)', block).group(1))
            description = re.search(r'Description:\s*(.*)', block, re.DOTALL).group(1).strip()
            scenes[scene_number] = description
    return scenes
