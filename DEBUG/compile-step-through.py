parent_dir = "~/ECTE250-2024"
scripts = ["/DEBUG/zap.py", "/MAIN_PROGRAM/startup.py"]

with open() as f:
    code = compile(f.read(), parent_dir + scripts, 'exec')
    exec(code, local_vars, global_vars)