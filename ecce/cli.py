import json
import os

import ecce.nave as nave
from ecce.constants import *

def export_nave(args):
    print(f'Writing to {NAVE_EXPORT_REF}')
    if os.path.isfile(NAVE_EXPORT_REF) is False:
        with open(NAVE_EXPORT_REF, 'w') as f:
            json.dump(nave.by_reference(), f)

    print(f'Writing to {NAVE_EXPORT_TOPIC}')
    if os.path.isfile(NAVE_EXPORT_TOPIC) is False:
        with open(NAVE_EXPORT_TOPIC, 'w') as f:
            json.dump(nave.by_topic(), f)


