class CommandWithAck:
    def __init__(self, menu_number: bytes, ack: bytes, response_size: int = 8) -> None:
        self.menu_number = menu_number
        self.ack = ack
        self.response_size = response_size


reset_defaults = CommandWithAck(b"\x02\xF0\x030D0100.", b"0D0100\x06.")
trigger_mode = CommandWithAck(b"\x02\xF0\x03091A00.", b"091A00\x06.")
presentation_mode = CommandWithAck(b"\x02\xF0\x03090901.", b"090901\x06.")
trigger = b"\x02\xF4\x03"
