function acquireEEG(name, time, mode)
% SYNTAX: acquireEEG(name, time, mode)
%
% name = filename
% time = recording time in seconds
% mode = any keyword from ['raw', 'meditation', 'attention', 'delta', 'theta', 'alpha1', 'alpha2', 'beta1', 'beta2', 'gamma1', 'gamma2']

assert((time <= 256), 'Very long EEG recording duration. Restart with shorter duration (< 256 seconds).')

%Create file to store acquired data
eegDataFile = fopen(strcat('C:\Users\Anna Reithmeir\Downloads\matlabdll64\matlabdll64\',name,'-',mode,'-',datestr(now,'DDmmyyyyHHMMSS'),'.csv'),'w');

%Preallocate buffer
data = zeros(1,256);

%COM Port Selection
portnum1 = 7;
comPortName1 = sprintf('\\\\.\\COM%d', portnum1);

% Baud rate for use with TG_Connect() and TG_SetBaudrate().
TG_BAUD_115200 = 115200;

% Data format for use with TG_Connect() and TG_SetDataFormat().
TG_STREAM_PACKETS = 0;

% Data type that can be requested from TG_GetValue().
TG_DATA_ATTENTION = 2;
TG_DATA_MEDITATION = 3;
TG_DATA_RAW = 4;
TG_DATA_DELTA = 5;
TG_DATA_THETA = 6;
TG_DATA_ALPHA1 = 7;
TG_DATA_ALPHA2 = 8;
TG_DATA_BETA1 = 9;
TG_DATA_BETA2 = 10;
TG_DATA_GAMMA1 = 11;
TG_DATA_GAMMA2 = 12;

%load thinkgear64 dll
loadlibrary('thinkgear64.dll');
fprintf('thinkgear64.dll loaded\n');

dllVersion = calllib('thinkgear64', 'TG_GetDriverVersion');
fprintf('thinkgear64 DLL version: %d\n', dllVersion );

% Get a connection ID handle to thinkgear64
connectionId1 = calllib('thinkgear64', 'TG_GetNewConnectionId');
if ( connectionId1 < 0 )
    error('ERROR: TG_GetNewConnectionId() returned %d.\n', connectionId1);
end

% Attempt to connect the connection ID handle to serial port "COM3"
errCode = calllib('thinkgear64', 'TG_Connect', connectionId1,comPortName1,TG_BAUD_115200,TG_STREAM_PACKETS );
if ( errCode < 0 )
    error('ERROR: TG_Connect() returned %d.\n', errCode);
end
fprintf( 'Connected. Reading Packets...\n' );

% Mode selection
switch mode
    case 'raw'
        flag = TG_DATA_RAW;
        modeTitle = 'Raw EEG: ';
    case 'attention'
        flag = TG_DATA_ATTENTION;
        modeTitle = 'Attention';
    case 'meditation'
        flag = TG_DATA_MEDITATION;
        modeTitle = 'Meditation';
    case 'delta'
        flag = TG_DATA_DELTA;
        modeTitle = 'Delta Power';
    case 'theta'
        flag = TG_DATA_THETA;
        modeTitle = 'Theta Power';
    case 'alpha1'
        flag = TG_DATA_ALPHA1;
        modeTitle = 'Alpha1 Power';
    case 'alpha2'
        flag = TG_DATA_ALPHA2;
        modeTitle = 'Alpha2 Power';
    case 'beta1'
        flag = TG_DATA_BETA1;
        modeTitle = 'Beta1 Power';
    case 'beta2'
        flag = TG_DATA_BETA2;
        modeTitle = 'Beta2 Power';
    case 'gamma1'
        flag = TG_DATA_GAMMA1;
        modeTitle = 'Gamma1 Power';
    case 'gamma2'
        flag = TG_DATA_GAMMA2;
        modeTitle = 'Gamma2 Power';
    otherwise
        disp('Invalid mode');
        flag = 15;
end

%To display in Command Window
disp('Reading Brainwaves');

Fs = 512; 

i=0;
j=0;

if (flag == 4)
    samples = time*Fs;
    while i < samples
        
        if (calllib('thinkgear64','TG_ReadPackets',connectionId1,1) == 1) %if a packet was read...
            
            if (calllib('thinkgear64','TG_GetValueStatus',connectionId1,flag) ~= 0)
                j = j + 1;
                i = i + 1;
                data(j) = calllib('thinkgear64','TG_GetValue',connectionId1,flag);
            end	
            
            if( j == 256 )
                fprintf(eegDataFile, '%f \n', data);
                figure(1);
                plot(data);
                title(modeTitle+string(0.5*(floor(i/256)-1))+'-'+string(0.5*floor(i/256))+' seconds');
                xlim([0, length(data)]);
                ylim([-1500, 1500]);
                j = 0;
            end
            
        end
        
    end
    
else
    delay = 6;
    samples = time+delay;
    figure;
    
    while i < samples
        
        if (calllib('thinkgear64','TG_ReadPackets',connectionId1,1) == 1) %if a packet was read...
            
            if (calllib('thinkgear64','TG_GetValueStatus',connectionId1,flag) ~= 0)
                j = j + 1;
                i = i + 1;
                data(j) = calllib('thinkgear64','TG_GetValue',connectionId1,flag);
                
                if ( j > delay )
                    fprintf(eegDataFile, '%d\n', round(data(j)));
                    plot(data(delay+1:samples), 'b-*');
                    title(modeTitle);
                    xlim([1, samples-delay]);
                    pause(1);
                end
                
                data(delay+1:samples)
                
            end
            
        end
        
    end
    
end

disp('Acquisition complete.')

%Release the comm port
calllib('thinkgear64', 'TG_FreeConnection', connectionId1 );

fclose(eegDataFile);

end

