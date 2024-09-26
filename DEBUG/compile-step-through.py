parent_dir = "~/ECTE250-2024"
scripts = ["/DEBUG/zap.py", 
            "/MAIN_PROGRAM/startup.py",
            "/MAIN_PROGRAM/main.py"]
with open() as f:
    code = []
    code.append(compile(f.read(), parent_dir.join(scripts), 'exec'))
    exec(code, local_vars, global_vars)