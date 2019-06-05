function readRAW
%run this function to connect and plot raw EEG data
%make sure to change portnum1 to the appropriate COM port

clear all
close all

data = zeros(1,256);    %preallocate buffer

portnum1 = 7;   %COM Port #
comPortName1 = sprintf('\\\\.\\COM%d', portnum1);


% Baud rate for use with TG_Connect() and TG_SetBaudrate().
TG_BAUD_57600 =      57600;


% Data format for use with TG_Connect() and TG_SetDataFormat().
TG_STREAM_PACKETS =     0;
TG_STREAM_5VRAW =        1;
TG_STREAM_FILE_PACKETS =  2;

% Data type that can be requested from TG_GetValue().
TG_DATA_RAW =         4;
TG_DATA_ATTENTION = 2; 


%load thinkgear dll
loadlibrary('thinkgear64.dll','thinkgear64.h');
fprintf('thinkgear64.dll loaded\n');

%get dll version
dllVersion = calllib('thinkgear64', 'TG_GetDriverVersion');
fprintf('ThinkGear DLL version: %d\n', dllVersion );


%%
% Get a connection ID handle to ThinkGear
connectionId1 = calllib('thinkgear64', 'TG_GetNewConnectionId');
if ( connectionId1 < 0 )
    error( sprintf( 'ERROR: TG_GetNewConnectionId() returned %d.\n', connectionId1 ) );
end;

% Set/open stream (raw bytes) log file for connection
errCode = calllib('thinkgear64', 'TG_SetStreamLog', connectionId1, 'streamLog.txt' );
if( errCode < 0 )
    error( sprintf( 'ERROR: TG_SetStreamLog() returned %d.\n', errCode ) );
end;

% Set/open data (ThinkGear values) log file for connection
errCode = calllib('thinkgear64', 'TG_SetDataLog', connectionId1, 'dataLog.txt' );
if( errCode < 0 )
    error( sprintf( 'ERROR: TG_SetDataLog() returned %d.\n', errCode ) );
end;

% Attempt to connect the connection ID handle to serial port "COM3"
errCode = calllib('thinkgear64', 'TG_Connect',  connectionId1,comPortName1,TG_BAUD_57600,TG_STREAM_PACKETS );
if ( errCode < 0 )
    error( sprintf( 'ERROR: TG_Connect() returned %d.\n', errCode ) );
end

fprintf( 'Connected.  Reading Packets...\n' );




%%
%record data

j = 0;
i = 0;
while (i < 5120)   %loop for 20 seconds
    if (calllib('thinkgear64','TG_ReadPackets',connectionId1,1) == 1)   %if a packet was read...
        
        if (calllib('thinkgear64','TG_GetValueStatus',connectionId1,TG_DATA_RAW) ~= 0)   %if RAW has been updated 
            j = j + 1;
            i = i + 1;
            data(j) = calllib('thinkgear64','TG_GetValue',connectionId1,TG_DATA_RAW);
        end
       
    end
     
    if (j == 256)
        figure(1);
        plotRAW(data);            %plot the data, update every .5 seconds (256 points)
        title('Raw EEG: '+string(0.5*(floor(i/256)-1))+'-'+string(0.5*floor(i/256))+' seconds');
        j = 0;
    end
    
end





%disconnect             
calllib('thinkgear64', 'TG_FreeConnection', connectionId1 );





