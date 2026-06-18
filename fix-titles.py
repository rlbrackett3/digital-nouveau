#!/usr/bin/env python3
"""Fix remaining titles: restore missing first character."""
import os, re

BLOG_DIR = "/root/user-files/projects/digital-nouveau/src/content/blog"

TITLE_FIXES = {
    'a-mindful-drawing-practice': ('A ', 'Mindful Drawing Practice'),
    'aesthetic-tuning-colony': ('A', 'esthetic Tuning :: Colony'),
    'architecture-of-2020': ('T', 'he Architecture of 2020'),
    'cholla-cactus-wood': ('C', 'holla Cactus Wood - Joshua Tree National Park'),
    'cocooning-ring-prototypes': ('C', 'ocooning Ring Prototypes'),
    'comics-architectural-narratives': ('C', 'omics :: Architectural Narratives'),
    'comics-beyond-fiction': ('C', 'omics Beyond Fiction :: [Trans-] FICTION 2020'),
    'concept-sketches-lighthouse': ('C', 'oncept Sketches for a Lighthouse'),
    'design-and-digital-design-2020': ('D', 'esign and Digital Design 2020'),
    'design-digital-design-fa20-crit-02': ('T', 'he Design and Digital Design FA20 :: Crit 02'),
    'drawing-018-veins': ('D', 'rawing 018 - Veins'),
    'drawing-020-laminar-erosion': ('D', 'rawing 020 - Laminar Erosion Process'),
    'drawing-021-summer-camp': ('D', 'rawing 021 - Summer Camp Landscapes'),
    'drawing-022-swelling-bud': ('D', 'rawing 022 - Swelling Bud'),
    'forming-rivers': ('F', 'orming Rivers'),
    'hyphae-mk2': ('H', 'yphae Simulation mk2'),
    'hyphae-mk3': ('H', 'yphae Simulation mk3'),
    'hyphae-simulation-mk2': ('H', 'yphae Simulation mk2'),
    'hyphae-simulation-mk3': ('H', 'yphae Simulation mk3'),
    'hyphae-simulations-mk1': ('H', 'yphae Simulations mk1'),
    'inspiring-june-flowers': ('I', 'nspiring June Flowers'),
    'keep-it-simple-stu': ('K', 'eep it Simple Stu***'),
    'landforms-craggs': ('L', 'andforms Craggs'),
    'learning-to-design-home': ('L', 'earning to Design @ Home :: Drawing and Modeling'),
    'make-beautiful-things': ('M', 'ake Beautiful Things'),
    'make-things': ('M', 'ake Things'),
    'motervation': ('M', 'otervation'),
    'not-quite-micro-worlds': ('N', 'ot Quite Micro Worlds'),
    'out-there': ('O', 'ut There :: And All Those Images In There'),
    'poetry-of-design': ('P', 'oetry of Design'),
    'pratt-final-review-design-1-fa2014': ('P', 'ratt Final Review Design 1 Fa2014'),
    'representational-analysis': ('R', 'epresentational Analysis :: Decomposition Drawing & Video'),
    'rock-dwellers': ('R', 'ock Dwellers'),
    'self-portraits-in-the-time-of-distance': ('S', 'elf Portraits in the Time of Distance'),
    'skyfi-april-2019': ('S', 'kyFi :: April 2019 :: Waning Dune & Into Ancillary Justice'),
    'skyfi-april-2020-agency': ('S', 'kyFi :: April 2020 :: Agency by William Gibson'),
    'skyfi-december-2019': ('S', 'kyFi :: December 2019 :: Ninefox Gambit'),
    'skyfi-july-2019': ('S', 'kyFi :: July 2019 :: Strange Stars'),
    'skyfi-june-2020': ('S', 'kyFi :: June 2020 :: Exploded View & New Dark Age (A Double Feature)'),
    'skyfi-november-2019': ('S', 'kyFi :: November 2019 :: Last and First Men & Star Maker Stories of Love'),
    'skyfi-october-2020-parable-of-the-sower': ('S', 'kyFi :: October 2020 :: Parable of the Sower - Octavia Butler'),
    'skyfi-september-2019': ('S', 'kyFi :: September 2019 :: Shadowbahn by Steve Erickson'),
    'staircases-perec': ('S', 'taircases - Georges Perec - Species of Space'),
    'suspended': ('S', 'uspended'),
    'technocrafting-digital-hand': ('T', 'echnocrafting the Digital Hand'),
    'the-computer-connection': ('T', 'he Computer Connection :: Alfred Bester'),
    'the-onnit-6-challenge-recap': ('T', 'he Onnit 6 Challenge Recap'),
    'the-owl': ('T', 'he Owl'),
    'travel-documents': ('T', 'ravel Documents'),
    'traveller-emergence': ('T', 'raveller :: Emergence'),
    'within-the-pixels': ('W', 'ithin the Pixels'),
}

count = 0
for slug, (expected_prefix, expected_rest) in sorted(TITLE_FIXES.items()):
    fpath = os.path.join(BLOG_DIR, f"{slug}.md")
    with open(fpath) as f:
        content = f.read()

    title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    if not title_match:
        print(f"  {slug}: no title found!")
        continue

    current = title_match.group(1)
    fixed_title = expected_prefix + expected_rest

    if current == fixed_title:
        print(f"  {slug}: already correct: '{current}'")
    else:
        content = content[:title_match.start(1)] + fixed_title + content[title_match.end(1):]
        with open(fpath, 'w') as f:
            f.write(content)
        count += 1
        print(f"  {slug}: '{current}' → '{fixed_title}'")

print(f"\nFixed {count} titles")
