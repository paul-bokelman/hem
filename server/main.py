import inquirer
from termcolor import colored
from lib.load import preflight
from lib import utils
from lib.input import Input
from lib.modes import inquisitive, compilation

preflight()

# header
print(f"\n{colored('Fathom', 'light_magenta', attrs=['bold', 'underline'])} {colored('— Understand efficiently.', 'dark_grey')}\n")

user_input = Input()

# initialize modes with user input
modes: dict[str, tuple[utils.Mode, str]] = {
    "Inquisitive": (inquisitive.Inquisitive(user_input), "be asked complex but concise questions"),
    "Compilation": (compilation.Compilation(user_input), "speak and have your thoughts compiled into notes"),
    # "Argumentative" -> future mode that will argue with the user to test their knowledge
}

# mode selection loop (main loop)
try:
    while True:
        mode_selection_question = [
            inquirer.List('mode',
                            message="Select mode",
                            choices=[utils.compose_q(key, value[1]) for key, value in modes.items()],
                        ),
        ]

        # mode selection
        mode_selection_answers = inquirer.prompt(mode_selection_question, raise_keyboard_interrupt=True)
        assert mode_selection_answers is not None
        mode, _ = utils.decompose_q(mode_selection_answers["mode"])

        if mode not in modes:
            print("\nInvalid mode selection. Please try again.")
            continue

        modes[mode][0].run()
except KeyboardInterrupt:
    print(f"\nThank you for using {colored('Fathom', 'light_magenta')}.")
    exit(0)