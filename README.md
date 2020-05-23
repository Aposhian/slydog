# Sly Dog
Third place project for The Y Hack 2019

Team-members: Aaron Aposhian, Adam Aposhian, Andrew Aposhian, terradactl

![Sly Dog Title Screen](https://raw.githubusercontent.com/Aposhian/slydog/master/assets/Sly%20Dog%20Title%20Screen.png)

***Derivative work of starpusher by Al Sweigart***

***This project uses code and a pretrained network from the [pytorch-chatbot](https://github.com/ywk991112/pytorch-chatbot) project by [ywk991112](https://github.com/ywk991112).***

***Original art assets by Aaron Aposhian***

### Running the game
1. Set up a Python 3 environment with all of the required dependencies.

2. Get the trained neural network file [here](https://www.space.ntu.edu.tw/navigate/s/D287C8C95A0B4877B8666A45D5D318C0QQY). Then place it in the root and use the following commands to move it and create the proper save directory where it should go.
    ```
    mkdir -p save/model/movie_subtitles/1-1_512
    mv 50000_backup_bidir_model.tar save/model/movie_subtitles/1-1_512
    ```

3. To play the game, run `python gameplay.py`

### Dependencies
* pygame
* pytorch
* dqdn
