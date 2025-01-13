import watchdog.events
import watchdog.observers
import time
import subprocess
import os


def run_manim():
    # Run manim with -pqm flags (preview quality, don't open media player)
    subprocess.run(["manim", "scene.py", "Collision", "-ql"])

    # Get the latest rendered file
    media_dir = "./media/videos/scene/480p15/"
    files = sorted(
        [f for f in os.listdir(media_dir) if f.endswith(".mp4")],
        key=lambda x: os.path.getmtime(os.path.join(media_dir, x)),
    )
    if files:
        latest_file = os.path.join(media_dir, files[-1])
        # Kill existing mpv process if any
        subprocess.run(["pkill", "mpv"], stderr=subprocess.DEVNULL)
        # Start mpv with position and size settings
        # Format: --geometry=<width>x<height>+<x>+<y>
        subprocess.Popen(
            [
                "mpv",
                "--loop",
                "--force-window=yes",
                "--geometry=50%+100%+100%",
                "--autofit=40%",
                "--focus-on=never",
                latest_file,
            ]
        )


class FileChangeHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"File {event.src_path} has been modified")
            run_manim()


if __name__ == "__main__":
    # Initial run
    run_manim()

    # Set up file watcher
    event_handler = FileChangeHandler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
