import logging
from typing import List
from .selector import LexicalSelector
# Import Grammar Physics to check flow

logger = logging.getLogger(__name__)

class Serializer:
    """
    Arranges selected words into a sentence.
    """
    def __init__(self, selector: LexicalSelector):
        self.selector = selector

    def serialize(self, pvi) -> str:
        """
        PVI: {subject: ID, verb: ID, object: ID}
        """
        # 1. Lexicalize
        subj_word_id = self.selector.select_word(pvi['subject'])
        verb_word_id = self.selector.select_word(pvi['verb'])
        obj_word_id = self.selector.select_word(pvi['object'])

        # 2. Retrieve Strings
        s_str = self._get_str(subj_word_id)
        v_str = self._get_str(verb_word_id)
        o_str = self._get_str(obj_word_id)

        # 3. Assemble (SVO default)
        return f"{s_str} {v_str} {o_str}."

    def _get_str(self, nid):
        n = self.selector.graph.get_neuron(nid)
        return n.payload.get('name', '???') if n else '???'
