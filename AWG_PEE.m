clear all;
clc;

Nsamples = 256; % Set The Number of Sample Points
RES    = 10;  % Set The DAC Resolution 10 or 8 bits
OFFSET = 0;   % Set An Offset Value For The DAC Output

%------------[ Calculate The Sample Points ]-------------
T = 0:((2*pi/(Nsamples-1))):(2*pi);
Y = sin(T);
Y = Y + 1;    
Y = Y*((2^RES-1)-2*OFFSET)/(2+OFFSET);
Y = round(Y);                 
plot(T, Y);
figure(1)
grid

% Periodic Sinc
figure(7)
Y2 = diric(T, 13);
Y2 = Y2 + 1;    
Y2 = Y2*((2^RES-1)-2*OFFSET)/(2+OFFSET);
Y2 = round(Y2);                  
plot(T, Y2);
grid

% Sawtooth
figure(2)
Y3 = sawtooth(T);
Y3 = Y3 + 1;    
Y3 = Y3*((2^RES-1)-2*OFFSET)/(2+OFFSET);
Y3 = round(Y3);                  
plot(T, Y3);
grid

% Triangular
figure(3)
Y4 = sawtooth(T, 0.5);
Y4 = Y4 + 1;    
Y4 = Y4*((2^RES-1)-2*OFFSET)/(2+OFFSET);
Y4 = round(Y4);                  
plot(T, Y4);
grid

% Square
figure(4)
Y5 = square(T, 50);
Y5 = Y5 + 1;    
Y5 = Y5*((2^RES-1)-2*OFFSET)/(2+OFFSET);
Y5 = round(Y5);                  
plot(T, Y5);
grid

%--------------[ Print The Sample Points ]---------------
fprintf('%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \n', Y);
 


%% test2

AMP = 10;

%%Time specifications:
f = 1000;     % signal frequency
sps = 256;    % samples per signal period
Fs = sps*f;  % samples per second
dt = 1/Fs;   % seconds per sample (time increment)
t = (0:dt:1); % 1 seconds of data (time)
sin_w =  AMP * sin(2*pi*f*t); % 1 second of data (sinus)
square_w = AMP* square(2*pi*f*t);
% Plot the signal versus time:
figure(6);
plot(t,sin_w);
xlabel('time (in seconds)');
title('Signal versus Time');
zoom xon;


new_vect = sin_w([1:256]);
no_amp = sin_w/10;
old_vect = no_amp([1:256]);

%conversion to the 0-3300 scale 
minValue = min(new_vect);
maxValue = max(new_vect);

% Calculate the scaling factor
scalingFactor = 3300 / (maxValue - minValue);

% Apply scaling to each element
scaledValues = (new_vect - minValue) .* scalingFactor

% Display the scaled values
%disp(scaledValues)

