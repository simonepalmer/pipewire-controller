import gi
import os

gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk

class Control:
    """Control class for business logic."""
    
    def __init__(self, buffer=64, samples=48000):
        self.buffer = buffer
        self.samples = samples
        self.control_window = None

    """If Pipewire is installed then apply settings, else show error"""

    def apply_settings(self):
        if os.popen('which pipewire').read() == '/usr/bin/pipewire\n':
            try:
                os.system(f'pw-metadata -n settings 0 clock.force-quantum {self.buffer}')
                self.control_window.label_buffer_settings.set_text(f"Sample size: {str(self.buffer)} samples")
                os.system(f'pw-metadata -n settings 0 clock.force-rate {self.samples}')
                self.control_window.label_sample_settings.set_text(f"Sample rate: {str(self.samples)} kHz")

                # I though about using the 'get_current_settings()' method to set the number here aswell
                # but since the button methods already sets the buffer and samples to intergers for the 
                # command to set the settings it seems stupid to not just use the same variables for the
                # label too

            except Exception as error:
                message = "Pipewire is installed but selected settings can't be applied"
                self.control_window.on_error(message, str(error))
        else:
            message = "Pipewire can't be found, use the command: 'which pipewire' to see if it is installed"
            self.control_window.on_error(message, "If not, install Pipewire and try again")

    """Gettings current settings to show in main window"""

    def get_current_settings(self):
        current_settings = os.popen('pw-metadata -n settings').read()
        settings_list = current_settings.split("'")

        buffer_i = settings_list.index('clock.force-quantum')
        buffer = settings_list[buffer_i+2]
        samples_i = settings_list.index('clock.force-rate')
        samples = settings_list[samples_i+2]

        if buffer == '0':
            buffer_i = settings_list.index('clock.quantum')
            buffer = settings_list[buffer_i+2]
        if samples == '0':
            samples_i = settings_list.index('clock.rate')
            samples = settings_list[samples_i+2]

        return buffer, samples

        # I found 2 problems in the previous version of this method.

        # 1st: If pipewire changes the order of their settings or in other ways change the format
        # of the output the settings_list[-4] could be something completely different, however, this
        # new way should be safer to not break since it's looking for the name of the settings it
        # wants the value for and then taking that index + 2 (+1 would be 'value:') 
        # Full line reads -: update: id:0 key:'clock.rate' value:'48000' type:'' :- so split at "'"
        # seems the best way to get the number by itself.
        #
        # I guess that if I would want to do it even more safe I could split at ":" and find the 
        # index after the matched index, then take that string and loop though it to remove every
        # character that is not a digit. So, safer but it I think it's a little bit convoluted
        # so I don't know if I like the trade off

        # 2nd: Pipewire has a "default" and a 'forced' settings of these values. To make it always
        # show the correct current setting it needs to check if the forced value is '0', which it 
        # will be after a reboot, and then take the default value when opening the program instead.

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

        self.label_buffer_settings = self.builder.get_object("label_buffer_settings")
        self.label_buffer_settings.set_text(f"Buffer size: {self.control.get_current_settings()[0]} samples")
        self.label_sample_settings = self.builder.get_object("label_sample_settings")
        self.label_sample_settings.set_text(f"Sample rate: {self.control.get_current_settings()[1]} kHz")

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

        # I'm not sure why every other method here need to use self.x
        # to work but this one can't have it, I think I have a lacking
        # understanding of how classes work which prevents me from 
        # figuring this out. Any input or explaination would be very helpful 

        # Also, I would very much like to have a button in this window
        # aswell connected to on_close_clicked() to close the entire app,
        # because there is not reason to keep it running if pipewire is
        # not installed. However, I probably spent 2 hours last week trying
        # to get a button to work without any progress, it was just doing
        # nothing so I skipped it for now

if __name__ == "__main__":
    control = Control()
    ControlWindow(control)
    Gtk.main()