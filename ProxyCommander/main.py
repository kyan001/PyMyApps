import os

import consoleiotools as cit
import pyperclip
import shellingham
import click


# Set environment variables through python script does not work. Run it in your shell manually.
__version__ = "1.1.1"

PROXY_IP = "127.0.0.1"
PROXY_PORT = 1088
PROXY_PROTOCOL = "http"
PROXY = (f"{PROXY_PROTOCOL}://" if PROXY_PROTOCOL else "") + f"{PROXY_IP}:{PROXY_PORT}"

OK = "[green]✓[/]"
KO = "[red]✕[/]"
ERR = "[bright_red]![/]"
PROXY_KEYS = {
    "PowerShell": ("HTTP_PROXY", "HTTPS_PROXY"),
    "Unix Shell": ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"),
}


def copy_cmd(cmd: str):
    pyperclip.copy(cmd)
    cit.info("Command is copied to clipboard!")


def get_shell_type():
    try:
        shell_name, shell_path = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        cit.err("Shell cannot detected.")
        cit.bye()
    if shell_name in ("pwsh", "powershell"):
        return "PowerShell"
    if shell_name in ("bash", "zsh", "csh", "tcsh", "sh"):
        return "Unix Shell"
    cit.err(f"`{shell_name} is not supported yet")
    cit.bye()


def set_var_command(key: str, value: str):
    shell_type = get_shell_type()
    if shell_type == "PowerShell":
        return f"$env:{key} = '{value}';"
    if shell_type == "Unix Shell":
        return f"export {key}='{value}';"


def unset_var_command(key: str):
    shell_type = get_shell_type()
    if shell_type == "PowerShell":
        return f"del env:{key};"
    if shell_type == "Unix Shell":
        return f"unset {key};"


def get_proxy_enable_command():
    shell_type = get_shell_type()
    return " ".join([set_var_command(key, PROXY) for key in PROXY_KEYS.get(shell_type)])


def get_proxy_disable_command():
    shell_type = get_shell_type()
    return " ".join([unset_var_command(key) for key in PROXY_KEYS.get(shell_type)])


def get_var_values(key: str):
    vals = {}
    has_value = None
    for index in (key, key.upper(), key.lower()):
        val = os.environ.get(index)
        if val:
            vals[index] = val
    if len(vals) == 0:
        has_value = False
    elif len(vals) == 1:
        has_value = True
    elif len(vals) == 2:
        v1, v2 = vals.values()
        has_value = True if v1 == v2 else None  # if not, ERROR
    else:  # len(vals) == 3
        v1, v2, v3 = vals.values()
        has_value = True if v1 == v2 == v3 else None  # if not, ERROR
    return has_value, vals


def get_var_conditions():
    def get_var_condition(key: str):
        has_value, vals = get_var_values(key)
        if has_value is False:
            return f"{KO} {key}"
        elif has_value is None:
            cit.warn("Conflicted Var Detected:", vals)
            deconflict_command = ' '.join([unset_var_command(key) for key in vals])
            cit.ask("Copy the unset command to deconflict and exit?", end=" ")
            cit.markdown(f"`{deconflict_command}`", end="")
            if cit.get_input(default="yes") == "yes":
                copy_cmd(deconflict_command)
                cit.bye()
            return f"{ERR} {key}: [bright_red]ERROR![/]"
        else:
            k, v = vals.popitem()
            return f"{OK} {k} {v}"

    shell_type = get_shell_type()
    keys = PROXY_KEYS.get(shell_type)
    if not keys:
        return None
    return [get_var_condition(key) for key in keys]


def is_proxy_enabled():
    shell_type = get_shell_type()
    keys = PROXY_KEYS.get(shell_type)
    if not keys:
        return None
    for has_value, vals in [get_var_values(key) for key in keys]:
        if has_value:
            return True
    return False


def show_proxy_status():
    proxy_enabled = is_proxy_enabled()
    var_conditions = get_var_conditions()
    cit.panel("\n".join(var_conditions), title="Proxy Status", subtitle=OK if proxy_enabled else KO, expand=False, style="info")
    return proxy_enabled


@click.group(invoke_without_command=True)
@click.pass_context
def main(context):
    if context.invoked_subcommand is None:
        proxy_enabled = show_proxy_status()
        cit.br()
        if not proxy_enabled:
            start()
        else:
            stop()


@main.command()
def status():
    show_proxy_status()


@main.command()
def start():
    cit.info("Proxy:", PROXY)
    cmd = get_proxy_enable_command()
    cit.panel(cmd or "Error", title="Proxy Enable Command", expand=False, style="info")
    copy_cmd(cmd)


@main.command()
def stop():
    cmd = get_proxy_disable_command()
    cit.panel(cmd or "Error", title="Proxy Disable Command", expand=False, style="info")
    copy_cmd(cmd)


if __name__ == '__main__':
    main()
