% Synthetic least-squares example; no extra toolbox is needed.
x = (1:5)';
y = [1.9; 4.1; 5.8; 8.2; 10.0];
X = [ones(size(x)), x];
beta = X \ y;
fitted = X * beta;
rmse = sqrt(mean((y - fitted).^2));
fprintf('intercept=%.4f, slope=%.4f\n', beta(1), beta(2));
disp(fitted);
fprintf('RMSE=%.4f\n', rmse);
