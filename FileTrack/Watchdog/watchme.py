import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import consoleiotools as cit
import consolecmdtools as cct


class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        result = event.src_path.removeprefix(cct.get_path(__file__).parent + "/")
        if event.is_directory:
            result = "📁" + result
        else:
            result = "📄" + result
        match event.event_type:
            case "created":
                cit.echo(f"[green]+ {result}[/]")
            case "deleted":
                cit.echo(f"[red]- {result}[/]")
            case "modified":
                cit.echo(f"[yellow]~ {result}[/]")
            case "moved":
                cit.echo(f"[blue]→ {result}[/]")
        return super().on_any_event(event)


event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, ".", recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
