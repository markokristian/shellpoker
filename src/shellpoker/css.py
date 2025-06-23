def css():
    return """
    #container {
        layout: vertical;
        height: 100%;
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
        text-style: bold;
    }
    #title {
        color: $text;
    }
    #version {
        color: $text-muted;
    }
    
    #main {
        layout: grid;
        grid-size: 2 1;
        grid-rows: 1fr auto;
    }

    #prizes {
        margin-left: 2;
        border: solid $accent;
    }

    #status {
        color: #FFD700;
        text-style: bold;
        margin-bottom: 1;
        padding: 0 2;
    }

    #hand {
        layout: horizontal;
        width: 100%;
        height: 7;
    }
    .card {
        layout: vertical;
        width: 8;
        height: 5;
        margin: 0 1;
    }
    .card-line {
        height: 1;
        width: 9;
        text-style: bold;
        color: white;
        background: white;
    }
    .card-line.hearts {
        color: red;
    }
    .card-line.diamonds {
        color: red;
    }
    .card-line.clubs {
        color: black;
    }
    .card-line.spades {
        color: black;
    }
    .card-line.obfuscated {
        color: #ad3939;
        background: red;
    }
    .card-line.obfuscated.mid {
        color: #ad3939;
        background: red;
    }

    #message {
        color: #ad3939;
        margin-bottom: 1;
        height: 5;
        padding: 0 2;
    }

    #action_input {
        border: solid #FFD700;
        color: #FFD700;
        background: $surface;
    }
    """
