# shellpoker

`shellpoker` is a command-line poker game written in python.

<img width="918" height="396" alt="sp v 0 1 0" src="https://github.com/user-attachments/assets/8e7205cf-93a2-4797-9d5a-aca2872306f6" />

## develop

### devcontainer

    git clone git+https://github.com/markokristian/shellpoker.git
    cd shellpoker
    code .
    open in devcontainer

Or use other devcontainer compliant IDE.

### just uv

    uv run shellpoker

## install and run

### with pip

    $ pip install git+https://github.com/markokristian/shellpoker.git --user
    $ shellpoker

### with docker

    docker run -it --rm python:3.12 bash -c "pip install git+https://github.com/markokristian/shellpoker.git && shellpoker"

## run fun simulation

    $ make simulate

    Simulating 5000 games with starting money of 20$ and target upside of 80$
    Happy (80$): 977 times (19.54%)
    Avg hands played: 27.51
    Avg final money: 17.51
    Total wins: 62397 (45.36%)
    Total money won: 487916
    Biggest win: 250
    Joker in win: 9159 times
    Bank earnings: 12449
    Win type distribution:
      Royal Flush         : 7
      Straight Flush      : 26
      Four of a Kind      : 947
      Full House          : 1824
      Flush               : 2332
      Straight            : 363
      Three of a Kind     : 14208
      Two Pairs           : 16317
      High Pair           : 26373

## license

This project is licensed under the MIT License.
