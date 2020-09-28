from phue import Bridge, PhueRegistrationException


class RegistrationException(object):
    pass


class HueManager:
    def __init__(self, ip):
        try:
            self._bridge = Bridge(ip)
        except PhueRegistrationException:
            raise RegistrationException

    def get_light_list(self):
        lights = self._bridge.get_light_objects('id')
        # l = map(lambda l: l.name, lights)

        return lights

    def set_light(self, light_id, parameter, value=None, transitiontime=None):
        self._bridge.set_light(light_id, parameter, value, transitiontime)
