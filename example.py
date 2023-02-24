import core

core = core.Core()

def test():
    print("test")

core.add_command("testtest", "test", test)

core()