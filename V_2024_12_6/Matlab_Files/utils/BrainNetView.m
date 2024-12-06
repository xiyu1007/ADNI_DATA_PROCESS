clc,clear,close;
% Add legend for BrainNet fig
addpath('Colors');
color = ColorMap(10,[],1);
RoiId = 1:1:10;  % 选择需要展示的ROI ID
figPath = 'BrainNetFig.fig'; % 启动BrainNet时不要有名为BrainNet.*的文件
infoPath = 'Template/ROITemplate/AAL3v1.csv';
info = getInfo(infoPath);
roiName = {};
for i = 1:length(RoiId)
    infoIndex = find([info{:, 1}] == RoiId(i));  % 查找对应的ROI
    roiName = [roiName; info{infoIndex, 2}];  % 使用info中的名称
end
assert(numel(RoiId) <= size(color,1) & numel(RoiId) <= numel(roiName));

%% 设置参数
interact = 1; % 可交互图例
view = 1;
rightMargin = 0.3;
legendSize = 0.05;  % 方框的边长 (正方形)
TokenSpace = 0.05;  % 方框与名称之间的间距
fontsize = 12;  % 字体大小
legendSpace = 0.1;  % 每个图例项之间的垂直间距
font = 'Arial';
%%
% run
figHandle = getfigHandle(figPath,view);
[axesHandles,~] = adjustPos(figHandle,0,rightMargin);
targetAxes = getLengedAX(figHandle,interact,rightMargin);
drawLenged(targetAxes,color,roiName,legendSize,legendSpace,TokenSpace,fontsize,font);

savefig(figHandle, 'BrainNetFigLenged.fig');
% close(figHandle);

%%
function figHandle = getfigHandle(figPath,view)
    if nargin < 2
        view = 0;
    end
    % 打开 .fig 文件
    tfigHandle = openfig(figPath, 'invisible'); % 加载图形文件
    figHandle = copyobj(tfigHandle, 0); 
    close(tfigHandle);
    % 删除原始menu,tool
    menus = findall(figHandle, 'Type', 'uimenu');
    delete(menus);
    toolbar = findall(figHandle, 'Type', 'uitoolbar');
    delete(toolbar);
    
    set(figHandle, 'MenuBar', 'figure', 'ToolBar', 'figure');
    set(figHandle, 'Position', get(0, 'DefaultFigurePosition'));
    set(figHandle, 'Name', 'Brain', 'NumberTitle', 'on');
    if view
        figHandle.Visible = 1;
    end
end

function [axesHandles,colors] = adjustPos(figHandle,getColor,rightMargin)
    if nargin <2 getColor = 0; end
    if nargin <3 rightMargin = 0.2; end
    % set(figHandle, 'Units', 'pixels'); % 坐标轴保持比例单位
    % 调整窗口大小
    figPos = get(figHandle, 'Position'); % [left, bottom, width, height]
    % 调整 fig 的宽度以包含空白区域
    newFigWidth = figPos(3) * (1 + rightMargin); % 增加宽度
    scaleFactor = figPos(3) / newFigWidth; % 缩放比例，用于保持 axes 比例不变
    figPos(3) = newFigWidth; % 更新 fig 的宽度
    set(figHandle, 'Position', figPos); % 应用新的宽度

    axesHandles = findobj(figHandle, 'Type', 'axes'); % 获取所有 axes
    % 调整每个 axes 的位置
    allColors = [];
    for i = 1:numel(axesHandles)
        % 获取当前 axes 的位置
        axPos = get(axesHandles(i), 'Position'); % [left, bottom, width, height]
        % 仅调整横向位置与宽度，保持比例不变
        newWidth = axPos(3) * scaleFactor; % 缩放宽度
        newLeft = axPos(1) * scaleFactor; % 横向位置同步缩放
        % 更新 axes 的位置
        set(axesHandles(i), 'Position', [newLeft, axPos(2), newWidth, axPos(4)]);

        if getColor
            % 获取颜色, 找到当前坐标轴中的所有 patch 对象
            patches = findobj(axesHandles(i), 'Type', 'patch');
            % 获取所有 patch 的 FaceColor 属性
            for j = 1:numel(patches)
                faceColor = get(patches(j), 'FaceColor');
                % 只保留 RGB 数值的颜色（排除 'none', 'flat' 等选项）
                if isnumeric(faceColor) && numel(faceColor) == 3
                    allColors = [allColors; faceColor]; % 收集颜色
                end
            end
        end
    end
    if getColor & ~isempty(allColors)
        % 去重并获取独立颜色
        colors = unique(allColors, 'rows');
        colors(ismember(colors, [0.95 0.95 0.95], 'rows'), :) = [];
        colors = flip(colors, 1);
    else
        colors = [];
    end
end

function targetAxes = getLengedAX(figHandle,interact,rightMargin)
    if nargin <3 rightMargin = 0.2; end
    % % 查找没有子对象的 axes
    % emptyAxesHandles = axesHandles(arrayfun(@(ax) isempty(get(ax, 'Children')), axesHandles));
    % 
    % % 如果存在没有孩子的 axes，则调整其位置填充右侧空白区域
    % if ~isempty(emptyAxesHandles)
    %     targetAxes = emptyAxesHandles(1); % 取第一个没有孩子的 axes
    % else
    %     % 如果没有空的 axes，则创建一个新的 axes
    %     targetAxes = axes('Parent', figHandle);
    % end
    
    targetAxes = axes('Parent', figHandle);
    set(targetAxes, 'Units', 'normalized'); % 坐标轴保持比例单位，pixels
    set(targetAxes, 'Position', [1 - rightMargin, 0, rightMargin, 1]);% [left, bottom, width, height]
    targetAxes.Visible ="on";
    axis(targetAxes, [0 0.5 0 1]); %[x_min, x_max, y_min, y_max]
    % 保持图形比例一致
    axis(targetAxes, 'equal');
    % 关闭坐标轴显示
    axis(targetAxes, 'off');
    if ~interact
        disableDefaultInteractivity(targetAxes);
    end
end

function drawLenged(targetAxes,colorMap,roiName,legendSize,legendSpace,TokenSpace,fontsize,font)
    n = size(colorMap,1);
    for i = 1:n
        % 绘制颜色方块 (正方形)
        % [left, bottom, width, height]
        rectangle('Parent', targetAxes,'Position', [0.1, (n-i)*legendSpace, legendSize, legendSize], ...
                  'FaceColor', colorMap(i, :), 'EdgeColor', 'none');
        
        % 在 targetAxes 上显示文本
        text('Parent', targetAxes, ...
             'Position', [0.1 + legendSize + TokenSpace, (n - i) * legendSpace + legendSize / 2], ...
             'String', roiName{i}, ...
             'VerticalAlignment', 'middle', ...
             'FontSize', fontsize, ...
             'FontName', font);
    end
    % fprintf('Added Lenged\n');
    % % 保存调整后的图形
    % savefig(figHandle, 'adjusted_with_invisible_patch_legend.fig');
end

function info = getInfo(infoPath)
    if nargin <1
        infoPath = 'Template/ROITemplate/AAL3v1.csv';
        % infoPath = 'Template/ROITemplate/aal3.csv';
    end

    % 读取数据并指定分隔符为分号
    infoData = readtable(infoPath, 'Delimiter', ';','TextType', 'string','ReadVariableNames', false);

    info = cell(size(infoData, 1), 4);
    for i = 1:size(infoData, 1)
        % 提取ROIid、ROIabbr、ROIname
        info{i, 1} = infoData{i,1};
        info{i, 2} = replace(num2str(infoData{i,2}),'_',' ');
        info{i, 3} = replace(num2str(infoData{i,3}),'_',' ');
        if size(infoData, 2) >= 4
            info{i, 4} = replace(num2str(infoData{i,4}),'_',' ');
        end
    end
end