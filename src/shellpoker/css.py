def css():
    return """
    #container {
        layout: vertical;
        height: 100%;
        padding: 0;
        align: center top;
    }

    #header {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr auto;
        height: 3;
        padding: 0 2;
        background: $surface;
        border-bottom: solid $accent;
    }

    #title,
    #version {
        content-align: center middle;
        text-style: bold;
    }

    #title {
        color: $text;
    }

    #version {
        color: $text-muted;
    }

    #status {
        content-align: center middle;
        color: #FFD700;
        text-style: bold;
        margin-bottom: 1;
    }

    #hand {
        content-align: center middle;
        background: #006400;
        text-style: bold;
        padding: 1 0;
        margin-bottom: 1;
    }

    #message {
        content-align: center middle;
        color: #ad3939;
        margin-bottom: 1;
        height: 5;
    }

    #action_input {
        border: solid #FFD700;
        color: #FFD700;
        background: $surface;
    }
    """
