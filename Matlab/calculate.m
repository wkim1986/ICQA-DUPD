function score = calculate(pdf, depth, range, alpha)

% I = index, S = sum, R = ratio,
% _S = start, _M = median, _E = end, _L = left, _R = right

score = 0;

I_S = range(1);
I_M = range(1) + ((range(2) - range(1)) / 2);
I_E = range(2);

S_L = 0;
S_R = 0;
for i = I_S+1:I_M
    S_L = S_L + pdf(i, 1);
end
for i = I_M+1:I_E
    S_R = S_R + pdf(i, 1);
end

if S_L + S_R == 0
    return
end

S = (S_L + S_R);
R_L = S_L / S;
R_R = S_R / S;

if R_L < R_R
    value = R_L;
else
    value = R_R;
end

coef = 0.5.^depth;

if depth ~= 8
    score = score + calculate(pdf, depth + 1, [I_S, I_M], R_L * alpha);
    score = score + calculate(pdf, depth + 1, [I_M, I_E], R_R * alpha);
end

score = score + coef * alpha * value;

if depth == 0
    score = score + 0.00390625;
end
