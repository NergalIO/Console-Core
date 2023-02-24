class Color:
    Reset         = '\033[0m'
    Bold          = '\033[1m'
    Faint         = '\033[2m'
    Italic        = '\033[3m'
    Underline     = '\033[4m'
    SlowBlink     = '\033[5m'
    RapidBlink    = '\033[6m'
    SwapBGaBG     = '\033[7m'
    Conceal       = '\033[8m'
    CrossedOut    = '\033[9m'
    Fraktur       = '\033[20m'
    BoldOff       = '\033[21m'
    ItalicOff     = '\033[23m'
    UnderlineOff  = '\033[24m'
    BlinkOff      = '\033[25m'
    InverseOff    = '\033[27m'
    ConcealOff    = '\033[28m'
    CrossedOutOff = '\033[29m'
    FGBlack       = '\033[30m'
    FGRed         = '\033[31m'
    FGGreen       = '\033[32m'
    FGYellow      = '\033[33m'
    FGBlue        = '\033[34m'
    FGMagenta     = '\033[35m'
    FGCyan        = '\033[36m'
    FGWhite       = '\033[37m'
    DefaultFG     = '\033[39m'
    BGBlack       = '\033[40m'
    BGRed         = '\033[41m'
    BGGreen       = '\033[42m'
    BGYellow      = '\033[43m'
    BGBlue        = '\033[44m'
    BGMagenta     = '\033[45m'
    BGCyan        = '\033[46m'
    BGWhite       = '\033[47m'
    DefaultBG     = '\033[49m'

class Columner:
    def __init__(self) -> None:
        pass
    
    def __call__(self, headers: list[str], data: list[list[str | int]]) -> str:
        columns = {}
        for header in headers:
            columns[header] = self.__get_row__(data, headers.index(header))
        lengths = [self.__getmaxlen__(header, columns[header]) for header in headers]
        
        result = "\n  "
        for i in range(headers.__len__()):
            result += f"{headers[i].upper()}{' ' * (lengths[i] - headers[i].__len__())}  "
        result += '\n\n  '
        
        for elem in data:
            for i in range(headers.__len__()):
                result += f"{elem[i]}{' ' * (lengths[i] - str(elem[i]).__len__())}  "
            result += '\n  '
        return result
            
    def __get_row__(self, data: list[any], krow: int) -> list[any]:
        return [elem[krow] for elem in data]
    
    def __getmaxlen__(self, header: str, data: list[str | int]) -> int:
        return max(header.__len__(), max([str(elem).__len__() for elem in data]))

class Command:
    def __init__(self, name: str, info: str, func) -> None:
        self.name = name
        self.info = info
        self.func = func
    
    def __call__(self, *args: any, **kwargs: any) -> any:
        return self.func(*args, **kwargs)

columner = Columner()

class Core:
    def __init__(self) -> None:
        self.commands = {
            "help": Command("help", "Getting help menu", self.__help__),
            "clear": Command("clear", "Getting help menu", self.__clear__),
            "info": Command("info", "Getting command info", self.__info__),
            "exit": Command("exit", "Close console", self.__exit__),
        }
        self._namelen = 5
        self.status = False
    
    def add_command(self, name: str, info: str, func) -> None:
        self.commands[name] = Command(name, info, func)
        self._namelen = max(self._namelen, name.__len__())
    
    def __call__(self) -> None:
        self.status = True
        try:
            while self.status:
                self.__command_handler__(input(" > "))
        except KeyboardInterrupt:
            print(f"\n{Color.FGCyan}Console closing...{Color.DefaultFG}")
    
    def __command_handler__(self, command: str) -> None:
        command, *values = command.split()
        try:
            command = self.commands.get(command, None)
            if command is None:
                raise ValueError(f"Unknown command '{command}'")
            command(*values)
        except Exception as error:
            self.__error_handler__(error)
    
    def __error_handler__(self, error: Exception) -> None:
        print(f"{Color.FGRed}  [~] Error '{Color.Underline}{error.__class__.__name__}{Color.UnderlineOff}' catched!")
        print(f"  [|] Message: {error}")
        print(f"  [~] Error message end {Color.Reset}")
    
    def __help__(self) -> None:
        print(f"{Color.FGCyan}  [~]       Help menu\n  [|]    Welcome to my program!")
        print(f"  [|]  Author: {Color.Underline}Nergal{Color.UnderlineOff} Version: {Color.Underline}0.1{Color.UnderlineOff}")
        lines = columner(['name', 'info'], [[name, command.info] for name, command in self.commands.items()]).split('\n')
        for line in lines:
            print('  [|]' + line)
        print("  [~] Help message end", Color.Reset)
    
    def __clear__(self) -> None:
        try:
            import os
            os.system('cls')
        except Exception as error:
            self.__error_handler__(error)
    
    def __info__(self, command: str) -> None:
        info = self.commands.get(command, None)
        if info is None:
            raise ValueError(f"Unknown command '{command}'")
        print(f"{Color.FGCyan}  [~] Info about command '{info.name}':")
        print(f"  [|] Info    : {info.info}")
        print(f"  [|] Function: {info.func}")
        print(f"  [~] Info message end {Color.Reset}")

    def __exit__(self) -> None:
        self.status = False

if __name__ == "__main__":
    core = Core()
    core()