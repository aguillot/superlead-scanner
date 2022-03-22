# superlead_scanner

Simple library to use a Superlead barcode scanner from Python

## Usage

In trigger mode
```python
import superlead_scanner

scanner = superlead_scanner.Scanner()

scanner.trigger_mode()

# block and return bytes
scanner.trigger_and_read()
```

In presentation mode

```python
import asyncio
import superlead_scanner

scanner = superlead_scanner.Scanner()

scanner.presentation_mode()

# block and return bytes, should be awaited in loops
asyncio.run(scanner.get_barcode())
```

Available settings (saved in ROM)
```python
scanner.reset_defaults_settings()

scanner.presentation_mode()
scanner.trigger_mode()

#set 500ms scan delay, default is 0
scanner.scan_delay_500ms()
```