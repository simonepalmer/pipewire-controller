import gi
import os

gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk

class Control:
    """Control class for business logic."""
    
    def __init__(self, buffer=64, samples=48000, status_command='start'):
        self.buffer = buffer
        self.samples = samples
        self.status_command = status_command
        self.control_window = None


    def apply_settings(self):

        # Check if pipewire is installed
        if os.popen('which pipewire').read() == '/usr/bin/pipewire\n':
            try:
                self.set_current_settings()
                self.show_current_settings()

            except Exception as error:
                message = "Pipewire is installed but selected settings can't be applied"
                self.control_window.on_error(message, str(error))
        else:
            message = "Pipewire can't be found, use the command: 'which pipewire' to see if it is installed"
            self.control_window.on_error(message, "If not, install Pipewire and try again")


    def set_current_settings(self):
        current_settings = self.get_current_settings()

        # Change settings if different from current values
        if str(self.status_command) != current_settings['status_word']:
            os.system(f'systemctl --user {self.status_command} pipewire.socket')
            os.system(f'systemctl --user {self.status_command} pipewire.service')

        if str(self.buffer) != str(current_settings['buffer_int']):
            os.system(f'pw-metadata -n settings 0 clock.force-quantum {self.buffer}')

        if str(self.samples) != str(current_settings['samples_int']):
            os.system(f'pw-metadata -n settings 0 clock.force-rate {self.samples}')


    def show_current_settings(self):
        current_settings = self.get_current_settings()

        # Settings current settings to the GUI labels
        self.control_window.label_status_settings.set_text(f"Status: {current_settings['status']}")
        self.control_window.label_buffer_settings.set_text(f"Buffer size: {current_settings['buffer']}")
        self.control_window.label_sample_settings.set_text(f"Sample rate: {current_settings['samples']}")


    def get_current_settings(self):
        if not os.popen('pw-metadata -n settings').read() == '':
            current_settings = os.popen('pw-metadata -n settings').read()
            settings_list = current_settings.split("'")
            
            buffer_index = settings_list.index('clock.force-quantum')
            if settings_list[buffer_index+2] == str(0):
                buffer_index = settings_list.index('clock.quantum')
            buffer = f"{settings_list[buffer_index+2]} samples"

            samples_index = settings_list.index('clock.force-rate')
            if settings_list[samples_index+2] == str(0): 
                samples_index = settings_list.index('clock.rate')
            samples = f"{settings_list[samples_index+2]} kHz"

            return {
                "status": "Active (Running)",
                "buffer": buffer,
                "samples": samples,
                "status_word": "start",
                "buffer_int": settings_list[buffer_index+2],
                "samples_int": settings_list[samples_index+2]
            }
        else:
            return {
                "status": "Suspended",
                "buffer": "Not active",
                "samples": "Not active",
                "status_word": "stop",
                "buffer_int": "Not set",
                "samples_int": "Not set"
            }


class ControlWindow:
    """ControlWindow class for GUI logic."""

    def __init__(self, control):
        self.control = control
        self.control.control_window = self

        self.builder = Gtk.Builder()
        self.builder.add_from_file("pipewire-control.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")
        self.window.set_title("Pipewire Controller")

        # Define radio buttons so they can be set not sensitive
        self.radio16 = self.builder.get_object('radio16')
        self.radio32 = self.builder.get_object('radio32')
        self.radio64 = self.builder.get_object('radio64')
        self.radio128 = self.builder.get_object('radio128')
        self.radio256 = self.builder.get_object('radio256')
        self.radio512 = self.builder.get_object('radio512')
        self.radio1024 = self.builder.get_object('radio1024')
        self.radio44 = self.builder.get_object('radio44')
        self.radio48 = self.builder.get_object('radio48')
        self.radio88 = self.builder.get_object('radio88')
        self.radio96 = self.builder.get_object('radio96')

        # Define and set labels so they can show the settings
        self.label_status_settings = self.builder.get_object("label_status_settings")
        self.label_buffer_settings = self.builder.get_object("label_buffer_settings")
        self.label_sample_settings = self.builder.get_object("label_sample_settings")

        self.control.show_current_settings()

        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)

    """apply & close buttons"""

    def on_close_clicked(self, clicked):
        Gtk.main_quit()

    def on_apply_clicked(self, clicked):
        self.control.apply_settings()
    
    """Buffer size radio buttons"""

    def on_radio16_toggled(self, toggled):
        self.control.buffer = 16

    def on_radio32_toggled(self, toggled):
        self.control.buffer = 32

    def on_radio64_toggled(self, toggled):
        self.control.buffer = 64

    def on_radio128_toggled(self, toggled):
        self.control.buffer = 128

    def on_radio256_toggled(self, toggled):
        self.control.buffer = 256

    def on_radio512_toggled(self, toggled):
        self.control.buffer = 512

    def on_radio1024_toggled(self, toggled):
        self.control.buffer = 1024

    """Samaple rate radio buttons"""

    def on_radio96_toggled(self, toggled):
        self.control.samples = 96000

    def on_radio88_toggled(self, toggled):
        self.control.samples = 88200

    def on_radio48_toggled(self, toggled):
        self.control.samples = 48000

    def on_radio44_toggled(self, toggled):
        self.control.samples = 44100

    """Pipewire status radio buttons"""

    def on_radioon_toggled(self, toggled):
        self.control.status_command = 'start'
        self.radio16.set_sensitive(True)
        self.radio32.set_sensitive(True)
        self.radio64.set_sensitive(True)
        self.radio128.set_sensitive(True)
        self.radio256.set_sensitive(True)
        self.radio512.set_sensitive(True)
        self.radio1024.set_sensitive(True)
        self.radio44.set_sensitive(True)
        self.radio48.set_sensitive(True)
        self.radio88.set_sensitive(True)
        self.radio96.set_sensitive(True)

    def on_radiooff_toggled(self, toggled):
        self.control.status_command = 'stop'
        self.radio16.set_sensitive(False)
        self.radio32.set_sensitive(False)
        self.radio64.set_sensitive(False)
        self.radio128.set_sensitive(False)
        self.radio256.set_sensitive(False)
        self.radio512.set_sensitive(False)
        self.radio1024.set_sensitive(False)
        self.radio44.set_sensitive(False)
        self.radio48.set_sensitive(False)
        self.radio88.set_sensitive(False)
        self.radio96.set_sensitive(False)

    """Showing error message"""

    def on_error(self, message, error):
        builder = Gtk.Builder()
        builder.add_from_file("pipewire-control.glade")
        window_error = builder.get_object("window_error")

        label_error = builder.get_object("label_error")
        label_error.set_text(message)
        label_hint = builder.get_object("label_hint")
        label_hint.set_text(error)

        window_error.show_all()

if __name__ == "__main__":
    control = Control()
    ControlWindow(control)
    Gtk.main()