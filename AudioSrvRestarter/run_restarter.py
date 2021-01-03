import consolecmdtools as cct


if __name__ == "__main__":
    if not cct.is_admin():
        cct.runas_admin(__file__)
    else:
        cct.run_cmd("net stop audiosrv")
        cct.run_cmd("net start audiosrv")
