import asyncio
import serial
import serial.tools.list_ports
import time


from superlead_scanner.commands import CommandWithAck
from . import commands

VENDOR_ID_7130N = 0x2DD6
DEVICE_ID_7130N = 0x26CA


class Scanner:

    BLOCK_DURATION = 0.5

    def __init__(
        self,
        vendor_id: int = VENDOR_ID_7130N,
        device_id: int = DEVICE_ID_7130N,
    ) -> None:
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.device = self._get_first_device()
        self.port = serial.Serial(self.device.device, timeout=None)

    def _get_first_device(self):
        devices_list = [
            d
            for d in serial.tools.list_ports.comports()
            if d.vid == self.vendor_id and d.pid == self.device_id
        ]
        if devices_list:
            return devices_list[0]
        else:
            raise Exception("no devices found")

    def _send_command_with_ack(self, command: CommandWithAck):
        self.port.reset_input_buffer()
        self.port.write(command.menu_number)
        return self.port.read(command.response_size) == command.ack

    def _block_until_data(self):
        while self.port.in_waiting == 0 and self._keep_blocking:
            time.sleep(self.BLOCK_DURATION)

    def reset_defaults_settings(self):
        return self._send_command_with_ack(commands.reset_defaults)

    def trigger_mode(self):
        return self._send_command_with_ack(commands.trigger_mode)

    def presentation_mode(self):
        return self._send_command_with_ack(commands.presentation_mode)

    def trigger_and_read(self) -> bytes:
        self.port.reset_input_buffer()
        self.port.write(commands.trigger)
        self._keep_blocking = True
        self._block_until_data()
        return self.port.read(self.port.in_waiting)

    async def get_barcode(self):
        self.port.reset_input_buffer()
        while self.port.in_waiting == 0:
            await asyncio.sleep(self.BLOCK_DURATION)
        return self.port.read(self.port.in_waiting)
