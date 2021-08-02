from phue import Bridge, PhueRegistrationException
from urllib.parse import urlparse
import discoverhue


class RegistrationException(BaseException):
    pass


class HueManager:
    def __init__(self, ip):
        try:
            self._bridge = Bridge(ip)
        except PhueRegistrationException:
            raise RegistrationException

    @staticmethod
    def get_bridge_list():
        bridges = discoverhue.find_bridges()
        return list(
            map(lambda bridge: {
                'id': bridge,
                'value': urlparse(bridges[bridge]).hostname
            }, bridges))

    def __innermap(self, lights):
        results = []
        for k in lights:
            results.append({
                'id': lights[k].light_id,
                'value': lights[k].name
            })
        return results

    def get_light_list(self):
        lights = self._bridge.get_light_objects('id')
        results = self.__innermap(lights)
        # results = map(lambda i, light: (
        #     {
        #         'id': i,
        #         # 'value': light['name']
        #     }
        # ), list(lights.items()))
        return results

    def set_light(self, light_id, parameter, value=None, transition_time=None):
        self._bridge.set_light(light_id, parameter, value, transition_time)
