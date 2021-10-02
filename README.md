# Motion Based WhiteBoard

Tracks the movement of user using Webcam and performs various operations such as writing, deletion and clearing the screen.

Workshop Documentation: [Link](https://docs.google.com/document/d/197V5TfCjr7cF0aZ59CXFSJNVlFJ3WyPL-vYOsldnSYQ/edit?usp=sharing)

## Requirments

```bash
pip install opencv-python
pip install numpy
```

## Installation

```bash
git clone https://github.com/mradul2/motion-based-whiteboard
```

## Usage

```bash
python3 main.py
```

- Use fluorescent yellow coloured object to instruct the program.
- Move the object in front of Webcam 
- The two modes (Pen and Eraser) are switched when Pen is taken away from the screen.
- Board is refreshed when the Pen is taken close to Webcam.

## Outputs

### Sample outputs in pen and eraser mode

#### Pen Mode

![Pen](assets/pen.png)

#### Eraser Mode

![Eraser](assets/eraser.png)
