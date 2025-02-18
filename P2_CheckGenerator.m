clc; clear all; close all;

load('model_checkpoint_Generator_Epoch2.mat', 'dlnetGenerator');

% prepare random latent vector
numLatentInputs = 256;
z = randn(1,1,numLatentInputs, 25, 'single'); % latent vector 25개
dlZ = dlarray(z, 'SSCB');
dlXGenerated = predict(dlnetGenerator, z);
dlXGenerated_dlX = predict(dlnetGenerator, dlZ);

% Plot generated images
h = figure;
h.Position = [950, 670, 560, 560];
tLay = tiledlayout(5, 5, "TileSpacing", "none", "Padding", "none");
I = imtile(rescale(dlXGenerated));
image(I);
xticklabels([]);
yticklabels([]);
axis tight;
axis off;

% Plot random latent vector
p = figure;
set(p, 'Position', [950, 670, 560, 560]);

tLay = tiledlayout(5, 5, 'TileSpacing', 'none', 'Padding', 'none');

I = squeeze(z); % (256×25)로 변환
size(I)
for i = 1:25
    subplot(5, 5, i);
    scatter(1:256, I(:,i), "filled");
    xlim([1,256]);
end
