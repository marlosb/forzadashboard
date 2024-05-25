'''
Copyright (c) 2022 Chris Faig

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
As I'm delighted with the beautiful and thorough copyright notice above I'm 
adding this simple and short one to inform that I have modified original code.
MarlosB 
'''

from abc import ABC, abstractmethod
import json
import logging
import socket
from struct import unpack

from logger import create_logger

logger = create_logger(__name__, logging.DEBUG)

IP_ADDRESS = '0.0.0.0' # all interfaces from the local machine
PORT = 6667

class ForzaDataPacket(ABC):
    '''Abstract class to handle Forza data packets.'''

    def __init__(self, 
                 data: bytearray,
                 driver_name: str) -> None:
        '''Initializes the ForzaDataPacket object.'''
        # criando os atributos do objeto e adicionando os valores recebidos
        self.attrirbutes_list = self.props + ['driver_name']
        for prop_name, prop_value in zip(self.props, unpack(self.format, data)):
            setattr(self, prop_name, prop_value)
        # atribuindo valor ao atributo driver_name
        setattr(self, 'driver_name', driver_name)

    def to_dict(self) -> dict:
        '''Converts the ForzaDataPacket object to dict.'''
        return {prop_name: getattr(self, prop_name) for prop_name in self.attrirbutes_list}
    
    def to_json(self) -> str:
        '''Converts the ForzaDataPacket object to JSON.'''
        return json.dumps(self.to_dict())

class Forza7Dash(ForzaDataPacket):
    '''Class to handle Forza Motorsport 7 Dash data packets.'''

    def __init__(self, 
                 data: bytearray,
                 driver_name: str) -> None:
        self.props = ['is_race_on', 'timestamp_ms',
            'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
            'acceleration_x', 'acceleration_y', 'acceleration_z',
            'velocity_x', 'velocity_y', 'velocity_z',
            'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
            'yaw', 'pitch', 'roll',
            'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
            'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
            'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
            'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
            'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
            'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
            'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
            'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
            'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
            'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
            'surface_rumble_FL', 'surface_rumble_FR',
            'surface_rumble_RL', 'surface_rumble_RR',
            'tire_slip_angle_FL', 'tire_slip_angle_FR',
            'tire_slip_angle_RL', 'tire_slip_angle_RR',
            'tire_combined_slip_FL', 'tire_combined_slip_FR',
            'tire_combined_slip_RL', 'tire_combined_slip_RR',
            'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
            'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
            'car_ordinal', 'car_class', 'car_performance_index',
            'drivetrain_type', 'num_cylinders',
            'position_x', 'position_y', 'position_z',
            'speed', 'power', 'torque',
            'tire_temp_FL', 'tire_temp_FR',
            'tire_temp_RL', 'tire_temp_RR',
            'boost', 'fuel', 'dist_traveled',
            'best_lap_time', 'last_lap_time',
            'cur_lap_time', 'cur_race_time',
            'lap_no', 'race_pos',
            'accel', 'brake', 'clutch', 'handbrake',
            'gear', 'steer',
            'norm_driving_line', 'norm_ai_brake_diff']
        self.format = '<iIfffffffffffffffffffffffffffffffffffffffffffffffffffiiiiifffffffffffffffffHBBBBBBbBB'
        super().__init__(data, driver_name)

class ForzaSled(ForzaDataPacket):
    '''Class to handle Forza Motorsport 2023 Sled data packets.'''

    def __init__(self, 
                 data: bytearray,
                 driver_name: str) -> None:
        self.props = [
            'is_race_on', 'timestamp_ms',
            'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
            'acceleration_x', 'acceleration_y', 'acceleration_z',
            'velocity_x', 'velocity_y', 'velocity_z',
            'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
            'yaw', 'pitch', 'roll',
            'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
            'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
            'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
            'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
            'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
            'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
            'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
            'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
            'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
            'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
            'surface_rumble_FL', 'surface_rumble_FR',
            'surface_rumble_RL', 'surface_rumble_RR',
            'tire_slip_angle_FL', 'tire_slip_angle_FR',
            'tire_slip_angle_RL', 'tire_slip_angle_RR',
            'tire_combined_slip_FL', 'tire_combined_slip_FR',
            'tire_combined_slip_RL', 'tire_combined_slip_RR',
            'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
            'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
            'car_ordinal', 'car_class', 'car_performance_index',
            'drivetrain_type', 'num_cylinders']
        self.format = '<iIfffffffffffffffffffffffffffiiiiffffffffffffffffffffiiiii'
        super().__init__(data, driver_name)

class Forza2023Dash(ForzaDataPacket):
    '''Class to handle Forza Motorsport 2023 Dash data packets.'''

    def __init__(self, 
                 data: bytearray,
                 driver_name: str) -> None:
        self.props = [
            'is_race_on', 'timestamp_ms',
            'engine_max_rpm', 'engine_idle_rpm', 'current_engine_rpm',
            'acceleration_x', 'acceleration_y', 'acceleration_z',
            'velocity_x', 'velocity_y', 'velocity_z',
            'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
            'yaw', 'pitch', 'roll',
            'norm_suspension_travel_FL', 'norm_suspension_travel_FR',
            'norm_suspension_travel_RL', 'norm_suspension_travel_RR',
            'tire_slip_ratio_FL', 'tire_slip_ratio_FR',
            'tire_slip_ratio_RL', 'tire_slip_ratio_RR',
            'wheel_rotation_speed_FL', 'wheel_rotation_speed_FR',
            'wheel_rotation_speed_RL', 'wheel_rotation_speed_RR',
            'wheel_on_rumble_strip_FL', 'wheel_on_rumble_strip_FR',
            'wheel_on_rumble_strip_RL', 'wheel_on_rumble_strip_RR',
            'wheel_in_puddle_FL', 'wheel_in_puddle_FR',
            'wheel_in_puddle_RL', 'wheel_in_puddle_RR',
            'surface_rumble_FL', 'surface_rumble_FR',
            'surface_rumble_RL', 'surface_rumble_RR',
            'tire_slip_angle_FL', 'tire_slip_angle_FR',
            'tire_slip_angle_RL', 'tire_slip_angle_RR',
            'tire_combined_slip_FL', 'tire_combined_slip_FR',
            'tire_combined_slip_RL', 'tire_combined_slip_RR',
            'suspension_travel_meters_FL', 'suspension_travel_meters_FR',
            'suspension_travel_meters_RL', 'suspension_travel_meters_RR',
            'car_ordinal', 'car_class', 'car_performance_index',
            'drivetrain_type', 'num_cylinders',
            'position_x', 'position_y', 'position_z',
            'speed', 'power', 'torque',
            'tire_temp_FL', 'tire_temp_FR',
            'tire_temp_RL', 'tire_temp_RR',
            'boost', 'fuel', 'dist_traveled',
            'best_lap_time', 'last_lap_time',
            'cur_lap_time', 'cur_race_time',
            'lap_no', 'race_pos',
            'accel', 'brake', 'clutch', 'handbrake',
            'gear', 'steer',
            'norm_driving_line', 'norm_ai_brake_diff',
            'tire_wear_FL', 'tire_wear_FR',
            'tire_wear_RL', 'tire_wear_RR',
            'track_ordinal']
        self.format = '<iIfffffffffffffffffffffffffffiiiiffffffffffffffffffffiiiiifffffffffffffffffHBBBBBBbbbffffi'
        super().__init__(data, driver_name)

    # Descrição do formato dos dados    
    # '<' é usado para especificar a ordem dos bytes 'little-endian'. Isso significa que o byte de menor valor é armazenado no endereço de memória mais baixo.
    # 'i' e 'I' são usados para especificar um número inteiro com sinal e sem sinal, respectivamente. Ambos são de 4 bytes (ou 32 bits).
    # 'f' é usado para especificar um número de ponto flutuante de precisão simples de 4 bytes (ou 32 bits).
    # 'H' é usado para especificar um número inteiro sem sinal de 2 bytes (ou 16 bits).
    # 'B' e 'b' são usados para especificar um número inteiro sem sinal e com sinal, respectivamente, de 1 byte (ou 8 bits).
    # Então, por exemplo, o formato 'sled_format' inicia com <iI, o que significa que os dados começam com um número inteiro de 4 bytes (com sinal), seguido por um número inteiro de 4 bytes (sem sinal).
    # Depois disso, vêm 63 'f's, o que significa que os próximos 63 campos são números de ponto flutuante de precisão simples de 4 bytes.
    # Em seguida, existem quatro 'i's, o que significa que os próximos quatro campos são números inteiros de 4 bytes (com sinal).
    # No caso do 'dash_format', os campos adicionais após os 'i's são uma combinação de números de ponto flutuante, números inteiros e bytes, conforme especificado pelos caracteres de formatação.

class ForzaDataReader:
    '''Class to handle Forza data packets.
    Args:
        ip (str) default "0.0.0.0" : IP address to listen on.
        port (int) default 1024: Port to listen on.
        filter_rate (int) default 10: Number of packets to skip between each packet processed.
    '''

    def __init__(self, 
                 driver_name: str,
                 ip: str = "0.0.0.0", 
                 port: int = 1024,
                 filter_rate: int = 8) -> None:
        '''Initializes the ForzaDataReader object.'''	
        self.driver_name = driver_name
        self.ip = ip
        self.port = port
        self.filter_rate = filter_rate
        logger.debug(f'\tForzaDataReader object created with driver_name: {self.driver_name}')

    def start(self) -> None:
        '''Starts the ForzaDataReader.'''
        # Configurando a conexão com o servidor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.packet_parsers = {232 : ForzaSled,
                               311: Forza7Dash,
                               331: Forza2023Dash}
        logger.debug(f'\tForzaDataReader started on {self.ip}:{self.port}')
        
    def read(self) -> ForzaDataPacket:
        '''Generator to read, format and output Forza data packets.
        Yields: ForzaDataPacket object.'''
        i = 0
        while True:
            # Aguardando por dados do jogo Forza
            data, addr = self.sock.recvfrom(1024)
            # Interpretando os dados recebidos usando a classe ForzaDataPacket
            data_len = len(data)

            try:
                parser = self.packet_parsers[data_len]
            except KeyError:
                logger.error(f'Unknown data packet length: {data_len}')
                logger.error(f'Packet data: {data}')
                yield None
                continue
            
            packet = parser(data, driver_name = self.driver_name)
            if i == self.filter_rate and packet.is_race_on == 1:
                i = 0
                logger.debug('ForzaDataReader.read() yield packet')
                yield packet
            elif i == self.filter_rate and packet.is_race_on == 0:
                i = 0
                logger.info('is_race_on is False')
                yield None
            i = i + 1