function score = ICQADUPD(img)

if ischar(img)
	img = imread(img);
end

[row, col, dimen] = size(img);
len = row * col;

if dimen ~= 1
    img = rgb2gray(img);
end

H = zeros(256, 1);
PDF = zeros(256, 1);

for x = 1:row
    for y = 1:col
        v = img(x, y);
        H(v+1, 1) = H(v+1, 1) + 1;
    end
end

for i = 1:256
    PDF(i, 1) = H(i, 1) / len;
%     fprintf('%d:%f\n', i-1, PDF(i, 1));
end

score = calculate(PDF, 0, [0, 256], 1);
