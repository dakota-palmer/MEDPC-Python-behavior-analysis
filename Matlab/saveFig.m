%% define function 
%to save and close individual figures

%2022-12-16 added figSize fxn


function saveFig(fig, figPath, figName, figFormats, figSize) %(time, signal)

    for format= 1:numel(figFormats)
        
%         %lots of code prior to 2022-12-16 won't have figSize argument, so use
%         %nargin to gate figSize setting
        if nargin<5
%             set(fig,'Position', get(0, 'Screensize')); %make the figure full screen before saving
        else
%             set(fig,'Position', figSize);
        end
         saveas(fig, strcat(figPath,figName,figFormats{format})); %save
    end
    
%     close(fig);

end


% %% Example use
% figure();
% title('test');
% figPath = 'C:\Users\Dakota\Desktop\testFigs\';
% 
% 
% saveFig(gcf, figPath, strcat('test','_', 'figure'),'.fig');
