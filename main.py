import tkinter as tk
import time
import math
import random

windowX = 800
windowY = 800

ballRad = 20
ballDia = ballRad * 2
ballSpeed = 5

scoreOn = True

colour1 = "#2D628A"
colour2 = "#F6C569"

direction1 = random.random() * 2 * math.pi
direction2 = random.random() * 2 * math.pi
running = True


def main():
    global direction1
    global direction2

    root = tk.Tk()
    root.geometry(f"{windowX}x{windowY}")
    root.title("Pong Thing")
    root.protocol("WM_DELETE_WINDOW", closeWindow)

    canvas = tk.Canvas(root, width=1000, height=1000, bg="white")
    canvas.pack(anchor=tk.CENTER, expand=True)

    sqL = round(windowX / ballDia)
    squares = [[0 for x in range(sqL)] for y in range(sqL)]
    cSquares = [[0 for x in range(sqL)] for y in range(sqL)]

    for i in range(0, sqL):
        for j in range(0, sqL):
            if i < sqL / 2:
                squares[i][j] = colour1
            else:
                squares[i][j] = colour2

    ball1 = canvas.create_oval(
        (windowX / 4) - ballRad,
        (windowY / 2) - ballRad,
        (windowX / 4) + ballRad,
        (windowY / 2) + ballRad,
        fill=colour2,
        outline=colour2,
    )

    ball2 = canvas.create_oval(
        ((3 * windowX) / 4) - ballRad,
        (windowY / 2) - ballRad,
        ((3 * windowX) / 4) + ballRad,
        (windowY / 2) + ballRad,
        fill=colour1,
        outline=colour1,
    )

    if scoreOn is True:
        score = canvas.create_text(
            (windowX / 2),
            windowY - (ballRad / 2),
            text="",
            anchor="s",
            justify="center",
            fill="white",
            font=("Helvetica", 16, "bold"),
        )

    drawSquares(canvas, squares, cSquares)

    canvas.tag_raise(ball1, "all")
    canvas.tag_raise(ball2, "all")
    while running:
        direction1 = moveBall(canvas, ball1, direction1, squares, colour1)
        direction2 = moveBall(canvas, ball2, direction2, squares, colour2)
        drawSquares(canvas, squares, cSquares)
        if scoreOn is True:
            updateScore(canvas, score, cSquares, colour1, colour2)
        canvas.tag_raise(ball1, "all")
        canvas.tag_raise(ball2, "all")
        if scoreOn is True:
            canvas.tag_raise(score, "all")
        root.update()
        time.sleep(0.001)


def moveBall(canvas: tk.Canvas, ball, direction: float, squares, colour):
    xInc, yInc = calcMove(direction)

    bBox = canvas.coords(ball)
    newBBox = [bBox[0] + xInc, bBox[1] + yInc, bBox[2] + xInc, bBox[3] + yInc]

    # print(f"oldPos: {bBox}, xInc: {xInc}, yInc: {yInc}, newPos: {newBBox}")

    collisionBox = False
    collisionWall = False
    # Check for colour collisions
    cX = newBBox[0] + ballRad
    cY = newBBox[1] + ballRad
    for i in range(0, 36):
        checkAngle = ((2 * math.pi) / 36) * i
        checkX = cX + (math.cos(checkAngle) * ballRad)
        checkY = cY + (math.sin(checkAngle) * ballRad)

        sqX = checkX / ballDia
        sqY = checkY / ballDia
        sqXInd = math.floor(sqX)
        sqYInd = math.floor(sqY)

        # clip to bounds
        sqXInd = 0 if sqXInd < 0 else sqXInd
        sqXInd = (
            round(windowY / ballDia) - 1
            if sqXInd > round(windowX / ballDia) - 1
            else sqXInd
        )

        sqYInd = 0 if sqYInd < 0 else sqYInd
        sqYInd = (
            round(windowY / ballDia) - 1
            if sqYInd > round(windowY / ballDia) - 1
            else sqYInd
        )

        # print(f"cX: {cX}, cY: {cY}, sqX: {sqX}, sqY: {sqY}")

        # Collision
        if squares[sqXInd][sqYInd] is not colour:
            squares[sqXInd][sqYInd] = colour

            # Move ball to collision location
            if checkAngle >= (3 * math.pi) / 4 and checkAngle < (5 * math.pi) / 4:
                # left collision
                newBBox[0] = (sqXInd * ballDia) + ballDia
                newBBox[2] = sqXInd * ballDia
                # print(
                #     f"Ball: {ball} collision left, direction: {direction}, check angle {checkAngle}"
                # )
            elif checkAngle >= math.pi / 4 and checkAngle < (3 * math.pi) / 4:
                # bottom collision
                newBBox[1] = (sqYInd * ballDia) - ballDia
                newBBox[3] = sqYInd * ballDia
                # print(
                #     f"Ball: {ball} collision bottom, direction: {direction}, check angle {checkAngle}"
                # )
            elif checkAngle >= (7 * math.pi) / 4 or checkAngle < math.pi / 4:
                # right collision
                newBBox[0] = (sqXInd - 1) * ballDia
                newBBox[2] = ((sqXInd - 1) * ballDia) - ballDia
                # print(
                #     f"Ball: {ball} collision right, direction: {direction}, check angle {checkAngle}"
                # )
            elif checkAngle >= (5 * math.pi) / 4 and checkAngle < (7 * math.pi) / 4:
                # top collision
                newBBox[1] = (sqYInd + 1) * ballDia
                newBBox[3] = ((sqYInd + 1) * ballDia) + ballDia
                # print(
                #     f"Ball: {ball} collision top, direction: {direction}, check angle {checkAngle}"
                # )

            if abs(math.cos(checkAngle)) > abs(math.sin(checkAngle)):
                newDirection = math.pi - direction
            else:
                newDirection = -direction

            collisionBox = True
            break

    # Check for boundary collisions
    if newBBox[0] < 0:
        newBBox[0] = 0
        newBBox[2] = ballDia
        newDirection = math.pi - direction
        collisionWall = True

    if newBBox[1] < 0:
        newBBox[1] = 0
        newBBox[3] = ballDia
        newDirection = -direction
        collisionWall = True

    if newBBox[2] > windowX:
        newBBox[2] = windowX
        newBBox[0] = windowX - ballDia
        newDirection = math.pi - direction
        collisionWall = True

    if newBBox[3] > windowY:
        newBBox[3] = windowY
        newBBox[1] = windowY - ballDia
        newDirection = -direction
        collisionWall = True

    # print(f"oldPos: {bBox}, xInc: {xInc}, yInc: {yInc}, newPos: {newBBox}")

    canvas.moveto(ball, newBBox[0] - 1, newBBox[1] - 1)

    # bBox = canvas.coords(ball)
    # print(f"moved to: {bBox}")

    if collisionBox is True:
        newDirection += (random.random() - 0.5) / 10

    if collisionBox is True or collisionWall is True:
        return newDirection
    else:
        return direction


def calcMove(direction):
    # print(f"calMove with {direction}")
    xInc = math.cos(direction) * ballSpeed
    yInc = math.sin(direction) * ballSpeed

    return xInc, yInc


def drawSquares(canvas: tk.Canvas, squares, cSquares):
    sqL = round(windowX / ballDia)
    for i in range(0, sqL):
        for j in range(0, sqL):
            if cSquares[i][j] != 0:
                canvas.itemconfigure(
                    cSquares[i][j], fill=squares[i][j], outline=squares[i][j]
                )
            else:
                cSquares[i][j] = canvas.create_rectangle(
                    i * ballDia,
                    j * ballDia,
                    (i + 1) * ballDia,
                    (j + 1) * ballDia,
                    fill=squares[i][j],
                    outline=squares[i][j],
                )
    return cSquares


def updateScore(canvas: tk.Canvas, scoreText, cSquares, colour1, colour2):
    count1 = 0
    count2 = 0
    sqL = round(windowX / ballDia)
    for i in range(0, sqL):
        for j in range(0, sqL):
            sq = canvas.itemconfigure(cSquares[i][j], "fill")
            if sq[4] == colour1:
                count1 += 1
            elif sq[4] == colour2:
                count2 += 1

    canvas.itemconfigure(scoreText, text=f"  day: {count2 : 3}  |  night: {count1 : 3}")


def closeWindow():
    global running
    running = False


main()
