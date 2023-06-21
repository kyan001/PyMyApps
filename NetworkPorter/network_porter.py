import consoleiotools as cit
import psutil


def get_pname_by_pid(pid: int) -> str:
    """Get process name by PID.

    Args:
        pid (int): PID

    Returns:
        str: process name
    """
    return psutil.Process(pid).name()


def get_pid_by_port(port: int) -> int:
    """Get PID by port.

    Args:
        port (int): port number

    Returns:
        int: PID. 0 if not found.
    """
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return conn.pid
    return 0


def ensure_pid_by_port(port: int) -> int:
    """Recheck port status.

    Args:
        port (int): port number

    Returns:
        int: PID. 0 if not found.
    """
    for i in range(3):
        pid = get_pid_by_port(port)
        if pid != 0:
            return pid
    return 0


if __name__ == '__main__':
    port = 1088
    cit.info(f'Port: {port}')
    pid = ensure_pid_by_port(port)
    if not pid:
        cit.warn(f'localhost:{port} is free, no PID found')
        cit.bye()
    pname = get_pname_by_pid(pid)
    cit.panel(f'localhost:{port} is used by `{pname}` (pid: {pid})')
    if cit.get_input('Stop this process?', default='Yes').lower() == 'yes':
        psutil.Process(pid).kill()
    else:
        cit.warn('Process not killed')
