clear all; clc;
fs = 999;
t = 0:1/fs:1;
figure(1)
grid on

% TRIANGLE WAVE
triangle = sawtooth(2*pi*t,0.5);
writematrix(triangle,"triangle.txt")
subplot(3,3,1), plot(triangle), title("TRIANGLE")

% TRIANGLE-SAW

t_tri= 0: 1/fs: 0.5;
t_saw= 0.5: 1/fs: 1;
tri_parte = sawtooth(2*pi*t_tri,0.5);
saw_parte = sawtooth (-(2*pi*t_saw));
tot=[tri_parte,saw_parte];
writematrix(tot,'trisaw.txt')
subplot(3,3,2), plot(tot), title("TRIANGLE SAW")

% SAW UP
sawup = sawtooth((2*pi*t));
writematrix(sawup,"sawup.txt")
subplot(3,3,3), plot(sawup), title("SAW UP")

% SAW DOWN
sawdown = flip(sawup);
writematrix(sawdown,"sawdown.txt")
subplot(3,3,4), plot(sawdown), title("SAW DOWN")

% SQUARE STANDARD
stdsquare = square(2*pi*t);
writematrix(stdsquare,"stdsquare.txt")
subplot(3,3,5), plot(stdsquare), title("SQUARE STANDARD")

% SQUARE 2
square2 = square(2*pi*t,25);
writematrix(square2,"square2.txt")
subplot(3,3,6), plot(square2), title("SQUARE 2")

% SQUARE 3
square3 = square(2*pi*t,12.5);
writematrix(square3,"square3.txt")
subplot(3,3,8), plot(square3), title("SQUARE 3")


