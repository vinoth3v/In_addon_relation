
''' one way or two way relation. eg: parent -> son, manager -> employee, friend -> friend '''



from .entity_relation_type import *
from .entity_relation import *
from .entity_relation_member import *
from .entity_relation_request import *
from .entity_relation_history import *
from .relation_manager import *
from .relation_link import *
from .relater import *
from .page import *
from .action import *
from .access import *
from .form import *

from .box import *
from .hook import *
from .lazy import *

from .ws_action import *

from .admin import *

# TODO: better cache
#@lru_cache(maxsize = 1000)
def get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id):
	
	manager = RelationManager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
	
	return manager


@IN.hook
def In_app_init(app):
	# set the relater

	IN.relater = Relater()
