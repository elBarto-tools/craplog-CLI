
from sys import argv
from time import sleep
from os.path import abspath

from crappy import aux
from crappy.git import gitPull
from crappy.get import versionCheck


class Crapup():
    def __init__(self, args:list ):
        # declare variables
        self.use_configs:   bool
        self.use_arguments: bool
        self.less_output: bool
        self.more_output: bool
        self.use_colors:  bool
        self.use_git: bool
        # paths
        self.crappath: str
        # messages
        self.text_colors:  dict
        self.MSG_elbarto:  str
        self.MSG_craplogo: str
        self.MSG_help:     str
        self.MSG_examples: str
        self.MSG_crapup:   str
        self.MSG_fin:      str
        self.TXT_crapup:   str
        self.TXT_fin:      str
        self.TXT_craplog:  str

        # initialize variables
        self.initVariables()
        self.initMessages()
        # parse arguments if not unset
        if self.use_arguments is True:
            self.parseArguments( args )
    
    
    def initVariables(self):
        """
        Initialize Crapup's variables
        This section can be manually edited to pre-set Crapup
          and avoid having to pass arguments every time
        """
        ################################################################
        #                 START OF THE EDITABLE SECTION
        #
        # HIERARCHY FOR APPLYING SETTINGS:
        #  - HARDCODED VARIABLES (THESE)
        #  - CONFIGURATIONS FILE
        #  - COMMAND LINE ARGUMENTS
        # THE ELEMENTS ON TOP ARE REPLACED BY THE ONES WHICH FOLLOW THEM,
        # IF HARDCODED VARIABLES ARE SET TO DO SO
        #
        # READ THE CONFIGURATIONS FILE AND LOAD THE SETTING
        # [  ]
        # IF SET TO 'False' MEANS THAT THE SAVED CONFIGS WILL BE IGNORED
        self.use_configs = True
        #
        # USE COMMAND LINE ARGUMENTS
        # [  ]
        # IF SET TO 'False' MEANS THAT EVERY ARGUMENT WILL BE IGNORED
        self.use_arguments = True
        #
        # REDUCE THE OUTPUT ON SCREEN
        # [ -l  /  --less ]
        self.less_output = False
        #
        # PRINT MORE INFORMATIONS ON SCREEN
        # [ -m  /  --more ]
        self.more_output = False
        #
        # USE COLORS WHEN PRINTING TEXT ON SCREEN
        # CAN BE DISABLED PASSING [ --no-colors ]
        self.use_colors = True
        #
        # UPDATE CRAPLOG USING git pull
        # [ --git ]
        # IF THE git IS NOT INITIALIZED YET, ASKS TO INITIALIZE ONE
        self.use_git = False
        #
        #                 END OF THE EDITABLE SECTION
        ################################################################
        #
        #
        # DO NOT MODIFY THE FOLLOWING VARIABLES
        #
        self.version = 3.07
        self.repo = "https://github.com/elB4RTO/craplog-CLI"
        self.crappath = ""
        self.MSG_elbarto = self.MSG_craplogo =\
        self.MSG_help = self.MSG_examples =\
        self.MSG_crapup = self.MSG_fin =\
        self.TXT_crapup = self.TXT_fin =\
        self.TXT_craplog = ""
        self.use_colors = True
        self.text_colors = aux.colors()


    def initMessages(self):
        """
        Bring message strings
        """
        # set-up colors
        if self.use_colors is False:
            self.text_colors = aux.no_colors()
        self.MSG_elbarto  = aux.elbarto()
        self.MSG_help     = aux.help( self.text_colors )
        self.MSG_examples = aux.examples( self.text_colors )
        self.MSG_craplogo = aux.craplogo()
        self.MSG_crapup   = aux.crapup( self.text_colors )
        self.MSG_fin      = aux.fin( self.text_colors )
        self.TXT_crapup   = "{red}c{orange}r{grass}a{cyan}p{white}UP{default}".format(**self.text_colors)
        self.TXT_fin      = "{orange}F{grass}I{cyan}N{default}".format(**self.text_colors)
        self.TXT_craplog  = "{red}C{orange}R{grass}A{cyan}P{blue}L{purple}O{white}G{default}".format(**self.text_colors)


    def parseArguments(self, args: list ):
        """
        Finalize Craplog's variables (if not manually unset)
        """
        n_args = len(args)-1
        i = 0
        while i < n_args:
            i += 1
            arg = args[i]
            if arg == "":
                continue
            # elB4RTO
            elif arg == "-elbarto-":
                print("\n%s\n" %( self.MSG_elbarto ))
            # help
            elif arg in ["help", "-h", "--help"]:
                print( "\n%s\n%s\n%s\n" %( self.MSG_craplogo, self.MSG_help, self.MSG_examples ))
            elif arg == "--examples":
                print( "\n%s\n%s\n" %( self.MSG_craplogo, self.MSG_examples ))
            # auxiliary arguments
            elif arg in ["-l", "--less"]:
                self.less_output = True
            elif arg in ["-m", "--more"]:
                self.more_output = True
            elif arg == "--no-colors":
                self.use_colors = False
            # git argument
            elif arg == "--git":
                self.git_update = True
            else:
                print("{err}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {rose}%s{default}"\
                    .format(**self.text_colors)\
                    %(arg))
                if self.more_output is True:
                    print("                 use {cyan}crapup --help{default} to view an help screen"\
                        .format(**self.text_colors))
                exit("")


    def welcomeMessage(self):
        """
        Print the welcome message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_crapup ))
            sleep(1)
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_crapup ))


    def exitMessage(self):
        """
        Print the exit message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_fin ))
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_fin ))
    
    
    def printError(self, err_key:str, message:str ):
        """
        Print an error message
        """
        print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} %s{default}"\
            .format(**self.text_colors)\
            %( err_key, message ))
    
    
    def exitAborted(self):
        """
        Print the abortion message and exit
        """
        print("{err}CRAPUP ABORTED{default}"\
            .format(**self.text_colors))
        if self.less_output is False:
            print()
        exit()


    def main(self):
        """
        Main function to call
        """
        # get Craplog's main path
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        self.crappath = crappath[:crappath.rfind('/')]
        
        # CRAPUP
        self.welcomeMessage()
        if self.use_git is True:
            # directly pull from the git
            gitPull( self )
        else:
            # just query the version number
            versionCheck( self )
        # everything went fine
        self.exitMessage()
    


if __name__ == "__main__":
    crapup = Crapup( argv )
    crapup.main()
    """
    failed = False
    try:
        crapup.main()
    except (KeyboardInterrupt):
        failed = True
    except:
        failed = True
    finally:
        pass"""