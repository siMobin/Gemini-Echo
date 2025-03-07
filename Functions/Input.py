from rich.console import Console
from prompt_toolkit import prompt
from rich.markdown import Markdown
from prompt_toolkit.key_binding import KeyBindings


def multiline_input():
    bindings = KeyBindings()

    # Shift+Down adds a new line
    @bindings.add("s-down")
    def _(event):
        event.current_buffer.insert_text("\n")

    # Enter submits the input
    @bindings.add("enter")
    def _(event):
        event.current_buffer.validate_and_handle()

    # Prompt user for input
    user_input = prompt(
        "\n•° ",
        multiline=True,
        key_bindings=bindings,
    )

    return user_input


# Test the function
if __name__ == "__main__":
    Console().print(
        Markdown("- Enter text (Shift+Down for new line, Enter to submit)"),
        style="bold Green",
    )
    print("\n", multiline_input())
