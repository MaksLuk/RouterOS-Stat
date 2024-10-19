import abc

from routeros_api import RouterOsApiPool
import ros_api


class Stat(abc.ABC):
    connection = None
    router = None
    
    @abc.abstractmethod
    def __init__(self, ip, port, username, password):
        pass
         
    @abc.abstractmethod
    def get_general_stat(self):
        '''
            получение данных о переданных и полученных пакетах/байтах за всё время (с момента последней перезагрузки роутера)
            вызывает метод _create_general_result для возврата результата в виде списка словарей
            в папке res на скринах 1.png и 1_1.png указаны все доступные атрибуты:
            - потерянные разными путями пакеты/байты
            - переданные по FastPath пакеты/байты
        '''
        pass

    @abc.abstractmethod
    def get_traffic_stat(self, interface):
        '''
            получение данных о текущей скорости (биты/пакеты) передачи данных в секунду по заданному интерфейсу
            принимает на вход имя интерфейса
            вызывает метод _create_traffic_result_dict для возврата результата в виде списка
            в папке res на скрине 2.png указаны все доступные атрибуты:
            - теряемые разными путями пакеты/байты
            - передаваемые по FastPath пакеты/байты
            ВАЖНО!!!
            в самом RouterOS возможно получить данные по всем интерфейсам, но через API получается вытягивать только по имени
            если попытаться задать interface = "", либо "all", "find", "[find]" - ошибка
            сам запрос к RouterOS возвращает массив всех подходящих под запрос интерфейсов, этот метод возвращает первый элемент массива
        '''
        pass

    def _create_general_result(self, data):
        result = [self._create_general_result_dict(i) for i in data]
        return result
     
    def _create_general_result_dict(self, data):
        result = {
            'name': data['name'],
            'type': data['type'],
            'status': data['running'],
            'mtu': data['mtu'],
            'actual-mtu': data.get('actual-mtu'),
            'mac-address': data['mac-address'],
            'last-link-up-time': data['last-link-up-time'],
            'sended-bytes': data['tx-byte'],
            'received-bytes': data['rx-byte'],
            'sended-packets': data['tx-packet'],
            'received-packets': data['rx-packet'],
        }
        return result
     
    def _create_traffic_result_dict(self, data):
        result = {
            'name': data['name'],
            'rx-bits-per-second': data['rx-bits-per-second'],
            'tx-bits-per-second': data['rx-bits-per-second'],
            'rx-packets-per-second': data['rx-packets-per-second'],
            'tx-packets-per-second': data['rx-packets-per-second'],
        }
        return result

    @abc.abstractmethod
    def disconnect(self):
        pass


class RouterOS_API_Stat(Stat):
    def __init__(self, ip, port, username, password):
        self.connection = RouterOsApiPool(ip, username=username, password=password, port=port, plaintext_login=True)
        self.router = self.connection.get_api()

    def get_general_stat(self):
        interfaces_data = self.router.get_resource('/interface').get()
        result = self._create_general_result(interfaces_data)
        return result

    def get_traffic_stat(self, interface):
        traffic_monitor = self.router.get_resource('/interface')
        response = traffic_monitor.call('monitor-traffic', {'interface': interface, 'once': ''})
        result = self._create_traffic_result_dict(response[0])
        return result

    def disconnect(self):
        self.connection.disconnect()


class Laiartus_ROS_API_Stat(Stat):
    def __init__(self, ip, port, username, password):
        self.router = ros_api.Api(ip, user=username, password=password, port=port)

    def get_general_stat(self):
        interfaces_data = self.router.talk('/interface/print')
        result = self._create_general_result(interfaces_data)
        return result

    def get_traffic_stat(self, interface):
        response = self.router.talk(f'/interface/monitor-traffic\n=interface={interface} =once=')
        result = self._create_traffic_result_dict(response[0])
        return result

    def disconnect(self):
        ''' в этой библиотеке не требуется disconnect '''
        pass


if __name__ == '__main__':
    print('ТЕСТ RouterOS_API_Stat')
    router1 = RouterOS_API_Stat('localhost', 8728, 'admin', 'admin')

    print('ИНТЕРФЕЙСЫ:')
    interfaces = router1.get_general_stat()
    print(interfaces)

    print('ТРАФИК:')
    for interface in interfaces:
        traffic_data = router1.get_traffic_stat(interface['name'])
        print(traffic_data)
    router1.disconnect()

    print()

    print('ТЕСТ Laiartus_ROS_API_Stat')
    router2 = RouterOS_API_Stat('localhost', 8728, 'admin', 'admin')

    print('ИНТЕРФЕЙСЫ:')
    interfaces = router2.get_general_stat()
    print(interfaces)

    print('ТРАФИК:')
    for interface in interfaces:
        traffic_data = router2.get_traffic_stat(interface['name'])
        print(traffic_data)

    
