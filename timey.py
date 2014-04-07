from AppKit import NSSound


class Sound:
    def __init__(self, file):
        self._sound = NSSound.alloc()
        self._sound.initWithContentsOfFile_byReference_(file, True)

    def play(self):
        self._sound.play()

    def stop(self):
        self._sound.stop()

    def is_playing(self):
        return self._sound.isPlaying()

# class CustomView(NSView):
#     n = 10

#     def X(self, t):
#         return (sin(t) + 1) * self.width * 0.5

#     def Y(self, t):
#         return (cos(t) + 1) * self.height * 0.5

#     def drawRect_(self, rect):
#         self.width = self.bounds()[1][0]
#         self.height = self.bounds()[1][1]
#         NSColor.clearColor().set()
        # NSRectFill(self.frame())


# class AppDelegate(NSObject):
#     def windowWillClose_(self, notification):
#         app.terminate_(self)

# class CustomWindow(NSWindow):
#     def awakeFromNib(self):
#         self.initialLocation = NSPoint()

    # def canBecomeKeyWindow(self):
    #     return True

    # def mouseDragged_(self, theEvent):
    #     screenFrame = NSScreen.mainScreen().frame()
    #     if screenFrame is None:
    #         sys.stderr.write('failed to obtain screen\n')
    #         raise RuntimeError
    #     windowFrame = self.frame()
    #     if windowFrame is None:
    #         sys.stderr.write('failed to obtain frame\n')
    #         raise RuntimeError
    #     currentLocation = self.convertBaseToScreen_(self.mouseLocationOutsideOfEventStream())
    #     newOrigin = NSMakePoint((currentLocation.x - self.initialLocation.x),
    #                             (currentLocation.y - self.initialLocation.y))
    #     if (newOrigin.y + windowFrame.size.height) > \
    #         (screenFrame.origin.y + screenFrame.size.height):
    #         newOrigin.y = screenFrame.origin.y + \
    #                       (screenFrame.size.height + windowFrame.size.height)
    #     self.setFrameOrigin_(newOrigin)

    # def mouseDown_(self, theEvent):
    #     windowFrame = self.frame()
    #     if windowFrame is None:
    #         sys.stderr.write('failed to obtain frame\n')
    #         raise RuntimeError
    #     self.initialLocation = \
    #         self.convertBaseToScreen_(theEvent.locationInWindow())
    #     self.initialLocation.x -= windowFrame.origin.x
    #     self.initialLocation.y -= windowFrame.origin.y


# def main():
#     global app
#     app = NSApplication.sharedApplication()
#     graphicsRect = NSMakeRect(100.0, 350.0, 450.0, 400.0)
#     myWindow = CustomWindow.alloc().initWithContentRect_styleMask_backing_defer_(
#         graphicsRect,
#         NSTitledWindowMask
#         | NSClosableWindowMask
#         | NSResizableWindowMask
#         | NSMiniaturizableWindowMask,
#         NSBackingStoreBuffered,
#         False)
#     # myWindow.setAlphaValue_(0.7)
#     myWindow.setBackgroundColor_(NSColor.clearColor())
#     myWindow.setBackgroundColor_(NSColor.whiteColor().set())
#     myWindow.setLevel_(NSStatusWindowLevel)
#     # myWindow.setOpaque_(False)
#     # myWindow.setHasShadow_(True)

#     myWindow.setTitle_('Tiny Application Window')
#     myView = CustomView.alloc().initWithFrame_(graphicsRect)
#     myWindow.setContentView_(myView)
#     myDelegate = AppDelegate.alloc().init()
#     myWindow.setDelegate_(myDelegate)
#     myWindow.display()
#     myWindow.orderFrontRegardless()
#     app.run()
#     print 'Done'


import rumps


INTERVAL_TIMER = (60) * 45
ICON_ACTIVE = 'statusItemIcon.png'
ICON_NOACTIVE = 'Icon-32.png'


class Pomodorro(object):
    """docstring for Pomodorro"""
    def __init__(self):
        self.started = False
        self.start = None
        self.now = None
        self.end = 0

    def go(self):
        self.started = True
        self.start = INTERVAL_TIMER + 1
        self.now = self.start
        self.end = 0

    def tick(self):
        self.now = self.now - 1
        if self.now <= self.end:
            self.stop()
            return self.end
        return self.now

    def stop(self):
        self.started = False
        self.start = None
        self.now = None
        self.end = 0


pomodorro = Pomodorro()
endTimerSound = Sound("Ship_Brass_Bell-Mike_Koenig-1458750630.mp3")


def timer_string(t):
    return "{:02d}:{:02d}".format(*divmod(t, 60))


# create a new thread that calls the decorated function every 1 second
@rumps.timer(1)
def updateUI(sender):
    if pomodorro.started:
        t = pomodorro.tick()
        timey.title = timer_string(t)
        if t == 0:
            timey.icon = ICON_NOACTIVE
            endTimerSound.play()
            # rumps.notification("Awesome title", "amazing subtitle", "hi!!1")


@rumps.clicked('Start timer')
def start_timer(_):
    pomodorro.go()
    timey.icon = ICON_ACTIVE


@rumps.clicked('Stop timer')
def stop_timer(_):
    pomodorro.stop()
    timey.title = '00:00'
    timey.icon = ICON_NOACTIVE

if __name__ == "__main__":
    timey = rumps.App("Timey", icon=ICON_NOACTIVE, title='00:00')
    timey.menu = [
        rumps.MenuItem('Start timer', icon='playback_play.png'),
        rumps.MenuItem('Stop timer', icon='playback_stop.png'),
        None
    ]
    timey.run()

