# Brick-Breaker
The classic brick breaker game in terminal from scratch without any special libraries such as pygame.

## Setup

1. <b>Installation</b><br />
pip3 install -r requirements.txt

2. <b>Execution</b><br />
python3 main.p

## Controls

1. `A` to move the paddle left.
2. `D` to move the paddle right.
3. `Space` to release the ball from the paddle.
4. `Q` to quit the game.

## Rules
1. You get 3 lives in the game.
2. Increase your score by breaking bricks.
3. Brick Color Scheme:
    * Green: Breakable but full health brick.
    * Orange: Breakable but half health brick.
    * Red: Breakable but quarter health brick.
    * Magenta: Unbreakable brick.
    * Blue: Exploding brick.
4. Hitting a green brick brings it to orange level. Orange turns to red. Red breaks/disappears.
5. Hitting an exploding brick makes it explode and directly break any other bricks close to it including unbreakable bricks.
6. Powerup Scheme:
    * "<=>" - Paddle Expand: Paddle width increases
    * ">=<" - Paddle Shrink: Padd width decreases
    * "2xO" - Ball Multiplier: Number of balls doubles
    * ">>>" - Fast Ball: Ball speed increases
    * "XXX" - Thru Ball: Ball can break any brick(even unbreakable) in 1 shot
    * "|_|" - Paddle Grab: Ball sticks to paddles when collides with paddle.
7. The above powerups can be active simultaneously in any combination as well. 
8. Each powerup lasts for about 15 seconds.
9. The game ends when player breakes all the breakable bricks or loses all lives.
10. The lesser the time taken, the higher the final score will be!